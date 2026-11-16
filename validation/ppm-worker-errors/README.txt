PPM export worker failure validation

The source branch contains two CLI tests with 24 subcases: standalone Zarr
arrays and OME-style groups, block sizes 1/2/4, with and without a stack.
The pixel data comes from the PHerc0800 rendered CT crop documented in
tests/data/PHerc0800/source.json. The planar PPM is generated test geometry.
The invalid inputs are temporary copies of those chunks truncated to eight
bytes. The original fixture is never modified.

Before: all 12 corrupt-input cases return success and write black TIFFs.
After: all 12 return an error before TIFF writing. Valid layer and stack
pixels match the source exactly in all 12 controls. The two JSON matrices
record four representative actual CLI runs before and after, including
pixel hashes and whether a decompression error was reported on stderr.

The combined patch reconstructs the exact tree recorded in validation.json
from baseline_commit. Its suite passes 8 methods / 131 real CT subcases;
16 separate transformation controls also pass. No raw terminal logs or
executables are public. Linux and macOS were not run.

Future.result() propagates the worker exception as documented by Python:
https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result
