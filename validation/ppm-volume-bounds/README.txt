PPM volume boundary validation

Pixel data comes from the PHerc0800 rendered CT crop documented in
tests/data/PHerc0800/source.json. PPM planes and sample coordinates are
generated test geometry, not extracted scroll surfaces.

Two regression methods cover 69 subcases: 45 direct interpolation samples
and 24 process_block cases, in memory and through a Zarr array. These cover
last faces/corners, negative/outside positions, a one-slice crop, and points
with zero normals whose stored coordinates are far away or NaN. The oracle
is SciPy RegularGridInterpolator with zero fill outside the sampled grid.
Before:15 pass,7 assertion failures,47 errors. After:69 pass.

Five real CLI exports per phase cover an interior plane, last Z plane,
corner, partially negative X, and an invalid surface hole. Four are wrong
before the fix; all match the independent reference afterward. The existing
worker-error issue makes the original CLI return success for black images;
that separate defect is fixed by fix/ppm-worker-errors.

The PNG displays actual TIFF pixels from the last-Z CLI exports, enlarged
by nearest neighbor and captioned by code. It is not a desktop screenshot.
It contains no cursor, path, or generated CT data. The original dimensions
are24x24; the corrected image preserves all576 nonzero CT pixels.

The combined patch reconstructs the exact tree in validation.json from
baseline_commit. The eight prepared contributions together pass10 methods
and200 real CT subcases, plus16 separate transformation controls.
Linux and macOS were not run. Raw logs and executables remain private.
