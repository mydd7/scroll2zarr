import hashlib
import json
from pathlib import Path
import subprocess
import sys
import argparse
import numpy as np
import tifffile
import zarr

parser = argparse.ArgumentParser()
parser.add_argument('converter', type=Path)
parser.add_argument('fixtures', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
case = args.output.resolve()
case.mkdir(exist_ok=False)
output = case / 'outputs'
output.mkdir()
python = Path(sys.executable)
converter = args.converter.resolve()
ct = np.stack([tifffile.imread(p) for p in sorted(args.fixtures.glob('*.tif'))])
normalized = ct.astype(np.float32) / 255
inputs = {'float32': normalized, 'float64': ct.astype(np.float64) / 255, 'channel': np.stack((normalized, normalized - 1)), 'uint16': ct.astype(np.uint16) * 257}
rows = []
for name, data in inputs.items():
    source = case / (name + '.zarr')
    if not source.exists():
        a = zarr.open(str(source), mode='w', shape=data.shape, chunks=data.shape, dtype=data.dtype)
        a[:] = data
    for algorithm in ['nearest', 'mean', 'max', 'gaussian']:
        destination = output / (name + '-' + algorithm + '.zarr')
        command = [str(python), str(converter), str(source), str(destination), '--nlevels', '3', '--algorithm', algorithm, '--num_threads', '2']
        if name == 'channel':
            command += ['--channel', '1']
        if name == 'uint16':
            command += ['--bytes', '1']
        with (output / (name + '-' + algorithm + '.log')).open('wb') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=60)
        if result.returncode:
            raise RuntimeError(name + ' ' + algorithm)
        levels = []
        for level in range(3):
            a = zarr.open(str(destination / str(level)), mode='r')[:]
            levels.append({'level': level, 'shape': list(a.shape), 'dtype': str(a.dtype), 'pixel_sha256': hashlib.sha256(a.tobytes()).hexdigest(), 'nonzero_voxels': int(np.count_nonzero(a)), 'min': float(a.min()), 'max': float(a.max())})
        expected = ct if name == 'uint16' else data[1] if name == 'channel' else data
        actual = zarr.open(str(destination / '0'), mode='r')[:]
        rows.append({'case': name, 'algorithm': algorithm, 'levels': levels, 'level0_equal_to_input': bool(np.array_equal(actual, expected)), 'level0_different_voxels': int(np.count_nonzero(actual != expected))})
report = {'source_file_sha256_lf': hashlib.sha256(converter.read_bytes().replace(b'\r\n', b'\n')).hexdigest(), 'ct_sha256': hashlib.sha256(ct.tobytes()).hexdigest(), 'cases': rows}
(case / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'runs': len(rows), 'level0_mismatches': sum(row['level0_different_voxels'] for row in rows)}))
