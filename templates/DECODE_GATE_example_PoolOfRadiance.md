# DECODE GATE — Pool of Radiance — **MET 12:16 MDT 2026-10-16** (all 10 items ticked with evidence; the coordinator declares it to the owner)

Gate rule (FOREMAN.md): no game-building until every item below is ticked. the coordinator declares the gate to the owner.

| # | item | evidence file(s) | state |
|---|---|---|---|
| 1 | Every code unit listed and owned (resident + 35 overlay units, sizes, load segments) | decode/LAYOUT.md, decode/listings/INDEX.md, decode/CROSSREF.md §1 | **TICKED 11:51** — LAYOUT + INDEX; CROSSREF §1 final unit->area map, each unit canonical once (9973d05) |
| 2 | Runtime + overlay manager understood (EXEPACK, TP 6.0 System/Crt/Dos/Overlay, FBOV stubs/fixups) | decode/LAYOUT.md, decode/rt/RT_LEDGER.md (verified H64/M22/L74) | **TICKED 11:51** — EXEPACK, FBOV 35 units, TP 6.0 runtime ledger verified |
| 3 | Every routine the game uses named with evidence or marked unknown | decode/pseudo/{ENGINE,ECL,VIEW,COMBAT,MAGIC,PARTY}.pas.md, decode/names/*.json, CROSSREF §5 unknown roll-up | **TICKED 12:16** — all 6 areas FINAL, independently verified (*_VERIFY.md) + fable-confirm; every #verify/#fable fix request APPLIED (last: #fable-6, 2a28a37); remaining placeholders = explicit unknowns listed in CROSSREF §5 |
| 4 | ECL script VM fully specified (all opcodes, operands, memory, vectors) | decode/ecl/ECL_VM.md, decode/pseudo/ECL.pas.md, decode/tools/ecldis.py | **TICKED 11:51** — 61/61 handlers, every opcode in data specified |
| 5 | All ECL scripts decoded | decode/ecl/scripts/*.md (29 FINAL) + INDEX.md | **TICKED 11:51** |
| 6 | Every data format specified | decode/data/{DAX,PICTURES,GEO,WALLDEF,MONSTERS,ITEM,ITEMS,SAVES}.md + INDEX.md, 784 PNGs | **TICKED 11:51** — all specs; CROSSREF §6: INDEX loaders 22/24 confirmed in code, SAVES field readers byte-checked |
| 7 | Screens inventoried | decode/pseudo/*_SCREENS.md (+ SCREENS_INDEX.md to write) | **TICKED 11:47** — 6/6 area SCREENS files + decode/pseudo/SCREENS_INDEX.md complete (all areas incl. PARTY, 8f6c194) |
| 8 | Verification passes | per-area self-check, *_ARGCHECK.md, *_VERIFY.md (independent Opus), acceptance/ref/DECODE_CHECKS.md (DOSBox-X oracle) | **TICKED 12:16** — self-checks, argcheck (0 MISMATCH x6), independent verifies x6, fable-confirm (27/30, no wrong formula/offset/constant), DOSBox oracle (35 checks; 3 DISAGREE applied); all fix requests APPLIED |
| 9 | Cross-area consistency (shared globals, names, call graph) | decode/CROSSREF.md | **TICKED 11:51** — CROSSREF.md final: names, 190 shared globals, call graph + main loop path, unknown roll-up, data<->code (9973d05) |
| 10 | Copy protection understood (code wheel, bypass flag) | PARTY.pas.md ov02; LAYOUT.md gate check (`START.EXE STING` skips credits + wheel) | **TICKED 12:16** — decoded (PARTY-ov02-01, Random(13) of CodeWheelTable; `STING` skip 0000:0102); build bypasses by default, wheel screen SU-06 shown on request = DOSBox 0 px |

## Known out-of-scope
- CFG.EXE / CFG.C (third-party a third-party starter), POOL.BAT.
