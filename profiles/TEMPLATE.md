# PROFILE — <toolchain name and version>

Status: untested | gate-passed | decoded | playable | oracle-verified
Proven on: <game, publisher, year> (one row per game)

## Identification
- How to recognise it (runtime strings, entry-point code, segment layout, file signatures), with byte evidence.

## Packing and overlays
- Packers seen and how they are undone (tool in `tools/`).
- Overlay scheme, header layout, how each unit is loaded into Ghidra at its own segment.

## The one layer
- What it is (runtime call table, overlay manager, script VM), where the dispatch table is, how calls are encoded, how many entries the game uses.

## Decompile notes
- Calling convention, parameter order, string format, sets/reals, idioms that mislead decompilers, and how listings are made readable (names map, runtime labels).

## Gate test result (Phase 0)
| Check | Result | Evidence |
|---|---|---|
| R1 statically recoverable | | |
| R2 high-level compiled / VM | | |
| R3 one layer located | | |
| R4 one data format round-trips | | |
| R5 oracle boots the game | | |

## Decode and build results
- Areas, function counts, time to decode gate, verification results, oracle results (screens matched / mismatched), playable state.

## Traps
- Anything that cost time, so the next game does not pay it again.

## Tools contributed
- Files added under `tools/` with one line each.
