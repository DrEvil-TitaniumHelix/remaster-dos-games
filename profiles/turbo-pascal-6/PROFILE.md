# PROFILE — Borland Turbo Pascal 6.0 with FBOV overlays (EXEPACK-packed)

Status: **decoded**; build in progress (title, first script text and explore screen match the original at 0 differing pixels)
Proven on: Pool of Radiance (SSI, 1988; this build's runtime string says 1983,91)

## Identification
- Runtime strings "Runtime error ", " at ", "Portions Copyright (c) 1983,91 Borland".
- Main program = a chain of far calls to unit initialisers (System first), then the program body.
- Overlay file starts with `FBOV`.

## Packing and overlays
- Microsoft EXEPACK: MZ with 0 relocations, entry stub `8C C0 05 10 00 0E 1F A3 04 00 03 06 0C 00 ...`; backwards RLE plus a packed relocation table after the "Packed file is corrupt" string. Undone by `tools/unexepack.py` (relocations recovered and checked).
- Turbo Pascal overlays: stub segments in the EXE + FBOV file with per-unit offsets, sizes and fixups. `tools/tpovl.py` lists and extracts every unit; each unit is loaded into Ghidra at its own segment with stubs rewritten as far-jump thunks.

## The one layer
- Two layers: (1) the TP System/Crt/Dos/Overlay runtime, identified by signature (ledger, about 160 routines, most generic); (2) in Gold Box games the **ECL event-script VM** (61 opcodes, dispatch table in an overlay unit). Decoding the VM makes all event scripts readable data.

## Decompile notes
- Ghidra decompiles TP code coherently once the DS segment and overlay segments are set.
- **Pascal pushes parameters left to right: decompiles show them reversed.** Re-check every call against the callee's declaration: this was the one systematic error class an independent Fable spot-check found.
- Strings are length-prefixed (Pascal strings); sets and 6-byte reals appear in the runtime.

## Gate test result
| Check | Result |
|---|---|
| R1 | EXEPACK + FBOV handled in hours |
| R2 | yes, naive compiler |
| R3 | runtime ledger + ECL VM |
| R4 | DAX container (1,245 records verify), pictures, maps, monsters, saves |
| R5 | DOSBox-X headless, title matches 0/64000 px |

## Decode and build results
- 1,347 functions; all areas final about 3h20 after start; decode gate met about 5-6 hours after start; entirely on Opus + codex lanes, 0 refusals.
- Independent Fable spot-check: 27/30 routines agree, 1 minor, 2 wrong (both call-shape errors); 7/8 opcodes agree; 3/3 hard formulas agree.
