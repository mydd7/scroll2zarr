Converter input path validation

The overwrite flow in the TIFF decompressor and both volume converters
could remove an output that contains its input. The source would then be
gone before it was read. Missing inputs could also discard prior output.
A common resolved-path check now guards all three tools before deletion.
Local Zarr paths and file:// paths are normalized through fsspec. Explicit
pyramid rebuilds still ignore the input argument and preserve level0.

All reproductions use fresh owned temporary directories. The resolved
output argument is asserted to remain below that owned directory before
running the old deletion paths. Pixel data is the documented PHerc0800
rendered CT crop. Decompression controls use three LZW TIFF copies;
conversion controls use the first two fixture images and their Zarr copy.

Fifteen destructive configurations lose files before and preserve every
existing relative-path/SHA256 pair after. The CLI matrices record actual
exit codes, lost file names and counts. Afterward each invalid case exits2
before modifying any file. Original scans and existing user outputs are
never used for the deletion reproductions. Raw terminal logs stay private.

Twenty-five positive controls preserve CT pixels, including LZW decoding,
new/sibling/child outputs, plain Zarr and OME, file:// input, HTTP/cached-HTTP input,
and both higher-level rebuild modes. Rebuilds retain level0 file hashes.
The HTTP control serves the same real CT store on a local test server.

Six regression methods cover40 subcases. Before25 pass and15 fail;
after all40 pass. The nine contributions together pass16 methods/240 real
CT subcases plus16 transformation controls. The combined patch reconstructs
the exact recorded tree from baseline_commit. Linux and macOS were not run.
The path preflight does not validate every possible input metadata or codec
failure, or make an otherwise valid overwrite transactional.
