# PROFILE — Microsoft QuickBASIC 3.00 (BRUN30 runtime, chained modules)

Status: **oracle-verified**
Proven on: Star Command (SSI, 1988): 7 modules + BRUN30.EXE

## Identification
- Each module is a small MZ stub that checks a `bz` (0x7A62) marker and loads `BRUN30.EXE` ("Must be a QuickBASIC 2.00 compiled module", "USERLIB.EXE" strings).
- Module header of 0x40 bytes in the code segment: size word in paragraphs, `bz` marker, 8-char module name.

## Packing and overlays
- None. Modules CHAIN to each other; shared state through a COMMON array.

## The one layer
- Every BASIC statement compiles to `INT 3Dh / 3Eh / 3Fh` + one inline byte = a runtime call through tables in BRUN30 (at 0x171 / 0x243 / 0x38D in this build). The game used 140 distinct routines; a few take one extra inline byte.
- Naming all 140 (ledger with H/M/L confidence) turns every module listing into near-BASIC.

## Decompile notes
- Ghidra cannot follow the module code from the stub entry: code starts at module offset 0x40 and has no static path from the entry. A runtime-call-aware disassembler (qbdis-style) is the right tool; Ghidra is used for the runtime itself.
- Singles are Microsoft Binary Format (MBF), not IEEE.
- Graphics: BSAVE'd GET arrays (CGA 2bpp, EGA 4-plane).
- Watch: PUT verb codes, `ABS` idiom (looks like negation), folded constant array indexes: all three were decode errors found only by the oracle.

## Gate test result
| Check | Result |
|---|---|
| R1 | yes, no packing |
| R2 | yes, naive compiler |
| R3 | runtime tables found same day |
| R4 | sprite banks + text data decoded |
| R5 | DOSBox-X headless, EGA machine |

## Decode and build results
- Decode gate in about 9 hours with up to 6 lanes; playable v1 overnight; 83/83 acceptance screens; 60/62 oracle reference rows PASS, 0 FAIL.
- Build: verified pseudocode translated mechanically (bas2js-style) into an HTML5/JS engine.
