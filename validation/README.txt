Scroll2zarr validation evidence

The TIFF fixtures retain actual CT intensities. Their source URLs, crops
and SHA256 hashes are committed beside them under tests/data/.
PHerc0800 uses a rendered surface volume from the public masked scan.
PHercParis4 uses an original uint16 scan slice, with no intensity rescaling.

The three comparison images are made from actual before/after arrays.
Their display scales and any amplification of differences are labelled.
visual-proof.json records the image provenance and the difference counts.

validation-excerpts.png is a native Notepad screenshot of excerpts from
saved validation logs, not a terminal screenshot or a live execution.
validation-excerpts.txt contains the same text. Application chrome was
cropped out, and a black rectangle covers the computer-use cursor and its
halo in otherwise blank space. No result text was changed or covered.

JSON files record the real-data checks. Windows and CPU were tested.
The conda installation file was updated but conda was not executed.
No speedup, improved ink accuracy or letter discovery is claimed.
The raw screenshots and full logs remain private outside this directory.
