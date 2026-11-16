Windowed Zarr copy on real PHerc0800 CT data

The comparison shows actual output arrays from the CLI. Before the fix,
the process exits with a broadcast shape error and leaves a partial store.
After the fix, every source voxel matches exactly and the eight columns
beyond the input stay zero. Each 32x40 slice is enlarged by nearest-neighbor
sampling; intensities are unchanged. PNG metadata is empty.

The JSON matrices cover compressed/uncompressed, simple/OME inputs and
two output chunk sizes. The eight multichannel checks use adjacent real CT
slabs. All control results and the source fixture hashes are recorded.

The combined controls use source tree 90a221db8efdcaf6a0899829566a72ea6e2c15d6.
Apply combined-validation.patch on scroll2zarr commit 56c0bd9c83ea071ef41210497ba5faacebb01613
to reproduce it. Applying this patch to a separate Git index produces
exactly that tree; it does not belong in the individual source PR.
