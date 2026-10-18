# Lane: data — specify every data file format and extract assets

Read FOREMAN.md first. Work in `decode/data/` (create it). Originals: `<targets>\starcommand\starcoma\` (read-only).

Known: 78 .BAS + 16 .EGA files are BSAVE images (7-byte header: FD, seg, off, len) whose body is one or more QuickBASIC GET arrays: word width-in-bits, word height, then rows of 4 EGA bit-planes ((w+7)/8 bytes per plane per row); e.g. BIGSH-1.EGA = sprite 88x56 then 62x5. .BAS files appear to be the CGA/other-mode variants (BIGSH-1.BAS = 176x56 single array). Verify plane order/colour mapping by rendering to PNG (write PNG with zlib manually; no PIL assumed) with the standard EGA 16-colour palette; render both plane-order hypotheses and pick the one that produces a recognisable ship; record the evidence.

Output: `decode/data/SPRITES.md` (per file: arrays, sizes, which module loads it — grep the listings for the filename in the string-literal table of each module: literals are `len, descriptorAddr, text` in the module's constant area after the code), `decode/data/png/<file>_<n>.png`, `decode/data/STR_FILES.md` (the 4 .STR files: format + contents), `decode/data/BAT.md`, and `decode/data/MODULE_CONSTANTS.md` (every string literal per module with its descriptor address, so pseudocode lanes can name variables). Commit; 5-line status to STATUS.md.
