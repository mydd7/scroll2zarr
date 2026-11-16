Floating-point OME-Zarr export check

Motivation: export a normalized PHerc0800 CT crop without losing the values
that preprocessing produced. The source TIFFs and provenance are in the PR.
They contain real rendered CT, not generated voxel data. The float inputs
are explicitly derived from those uint8 TIFFs; no Lasagna field is claimed.

Before, floor division by one zeroed every normalized positive float voxel
at level 0. Pyramid generation also rounded fractional samples and treated
a negative block with maximum zero as empty. After, float32/float64 values
are copied exactly at level 0 and floating pyramid levels retain fractions.
Only the uint16-to-uint8 conversion still divides by256. Nonfloating
pyramid outputs retain rounding.

5 test methods cover28 data scenarios:3D/4D copying, positive and negative
normalized CT, all four resampling modes, float32/float64, and uint8,
uint16 and boolean controls.15 subcases fail on main; all pass after.
The float pyramid reference uses whole-array filtering in one source chunk.
The Gaussian boundary issue tracked in PR5 is separate from this change.

16 CLI processes per source version: float32, float64,4D channel extraction,
and uint16-to-uint8, each with nearest/mean/max/gaussian and3 output levels.
All16 fixed runs preserve level0 values. All files in the four integer
outputs, including metadata and compressed chunks, are byte-identical to
main. Source hashes and per-level value hashes are in validation.json.

Reproduce with the project's Zarr2 Python dependencies:
  python -m unittest discover -s tests -p test_float_volumes.py -v
  python reproduce.py /path/to/zarr_to_ome.py /path/to/tests/data/PHerc0800 NEW_OUTPUT
Run the second command once for each source version with a new output path.
It records value hashes and comparisons in results.json; raw CLI logs stay
in the local output directory and may include machine-specific paths.

Windows x64,Python3.12.10,2threads. These are correctness checks on a small
real crop, not a full-scroll throughput or ink-reading benchmark. Linux
and macOS were not executed. No native reader build is needed.
