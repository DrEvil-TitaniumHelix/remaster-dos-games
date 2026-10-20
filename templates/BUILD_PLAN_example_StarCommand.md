# BUILD PLAN — Star Command reproduction (phase 2)

Status: **FINAL 2026-10-15 18:40 (DECODE_GATE.md met). Build lanes start now (the owner: no go-ahead needed); the coordinator reports this plan to the owner.** Owner: Foreman. Ruling in force: SC-1 = B (same content, layout and behaviour per screen as the original in DOSBox; palette/resolution enhanced to 640x200 EGA 16-colour; the .EGA banks are the art source).

## 1. What is being built
A zero-install HTML5 game in `game/`: `index.html` + vanilla ES modules, no build step, runs from a file:// or any static host in Chrome on the handheld PC. Keyboard and Gamepad API. Everything the player sees is driven by the decode: `decode/pseudo/SCREENS_INDEX.md` (76 + PLBATTLE rows, ids CM/SU/PT/SP/IN/SB/PB), the module pseudocode `decode/pseudo/<MOD>.bas.md`, the CHAIN graph and shared-state map in `decode/pseudo/CROSSREF.md`, the data formats in `decode/data/`.

## 2. Engine architecture (`game/engine/`, one ES module each)
| module | responsibility | decode source |
|---|---|---|
| `display.js` | Logical framebuffer 320x200 of 4-bit colour indexes (the original's geometry: every module is SCREEN 1, PLBATTLE SCREEN 7). Rendered to a canvas at 640x400 (2x horizontal = the 640x200 EGA enhancement, 2x vertical for square-ish pixels), integer-scaled to the window, nearest-neighbour. EGA 16-colour palette table; per-module `PALETTE` remaps exactly as the originals do on EGA (STARTUP/SPACE/STARPORT `PALETTE 1,9: 2,4`; INSIDE `1,2: 2,6`; PLBATTLE native 16 colours). | SCREENS_INDEX.md "Palette per module"; SPRITES.md §3 |
| `text.js` | BASIC screen emulation: `LOCATE r,c`, `PRINT` (items, `;`, newline, scroll), `PRINT USING` (`##`, `###`, `#.##` as the modules use them), `COLOR fg,bg`, `CLS`, `KEY OFF`; 40x25 cells of 8x8 pixels (col c -> x = 8(c-1), row r -> y = 8(r-1)). 8x8 bitmap font as a data file (`assets/font8x8.json`, an open CGA-compatible font, licence noted in `game/ASSETS.md`). | STARTUP/SPACE/... `.bas.md` PRINT sites; RT_LEDGER LOCATE/PRINT rows |
| `sprites.js` | Sprite atlas loader + `put(bank, index, x, y, verb)` with the five BASIC verbs on the index framebuffer: OR, AND, PRESET (inverted copy), PSET (copy), XOR (RT_LEDGER 3E_58, byte-proven). `get(x1,y1,x2,y2) -> buffer` and `put(buffer, ...)` for the screen-capture arrays the modules use. **Data-driven (the owner/coordinator 2026-10-15):** sprites come from `assets/atlas.png` + `assets/atlas.json` (`{bank, index, x, y, w, h}` per sprite, plus a global `scale` factor = atlas pixels per logical pixel). No sprite data in code, so an upscaled or redrawn atlas with a different `scale` can be swapped in later without code changes. The art pass itself is deferred (the owner). | SPRITES.md, sprites_index.tsv, SCREENS_INDEX.md sprite columns |
| `input.js` | `INKEY$` semantics: a key queue returning the same codes the modules switch on (letters either case, extended codes for arrows, ENTER = 13, SPACE = 32, BACKSPACE, ESC); `INPUT` line editor for the few text prompts. Gamepad API mapping: d-pad/left stick = arrows, A = ENTER, B = ESC/N, X = SPACE, Y = Y(es); letter menus get a highlight cursor moved by the d-pad and confirmed with A, which injects the letter, so the module code stays identical for both devices. | SPACE.bas.md "Key map" (Cmd! 1..11 extended, 12..37 letters), each `_SCREENS.md` keys column |
| `audio.js` | `PLAY` MML interpreter (tempo, octave, length, notes, `MB` background queue) on a Web Audio square wave; `PLAY(n)` queue-length query; `SOUND`/`BEEP` if used. Sound-off flag A(93). | STARTUP music feeder, RT_LEDGER 3E_51 / 3D_44 |
| `state.js` | The COMMON array `G!()` as a `Float32Array(2601)` with named accessors generated from the CROSSREF.md index map (`state/gmap.json`), crew records, the 20 string arrays; load/save in the original CHARINFO.BAS BSAVE layout (MBF single <-> IEEE conversion) so the shipped save and DOSBox saves interoperate; browser persistence via localStorage/IndexedDB as a file store (`CHARINFO.BAS`, `IN-n`/`INMAP-n` arrays). | CROSSREF.md §2, DATA_FILES.md B, MODULE_CONSTANTS.md COMMON table |
| `data.js` | Loader for the converted data tables (`assets/data/*.json`: INFO.BAS tables, ENC*/ENCINFO/MISSION records, NAME/CHARNAME strings, map banks) with the column semantics from DATA_FILES.md §D. | DATA_FILES.md, CROSSREF.md §3 |
| `timer.js` | `TIMER`-based delays with the original constants (A(86) StdDelay, A(88) Delay) instead of the CPU calibration loop; frame scheduler (requestAnimationFrame) that runs the module coroutines. | STARTUP.bas.md calibration, SPACE delay 8324 |
| `chain.js` | `CHAIN` = switch active module with `G!()` intact (EntryMode! G!(2227), ChainArg! and friends per CROSSREF §1.3). Floppy stubs (.STR, screen ST-01) are **not built**: the reproduction implements the hard-disk configuration (Foreman decision 2026-10-15, reversible). | CROSSREF.md §1 |

Modules are written as async functions over an `await`-able engine API (`await input.key()`, `await timer.wait(ms)`) so each `.bas.md` flow transcribes almost line by line, labels become functions or loop states, and GOSUBs become calls.

## 3. Asset pipeline (`tools/`, Python 3.13, run once, outputs committed)
1. `tools/build_atlas.py`: reads every `.EGA` bank (and the `.BAS` banks for CGA-only sprites that have no EGA twin, converted through the EGA palette remap) with `decode/data/tools/bsave.py`, packs all GET arrays into `game/assets/atlas.png` (16-colour indexed PNG) and writes `atlas.json` (`scale: 1`). Every entry keyed by `bank` (file stem) and `index` exactly as `sprites_index.tsv` numbers them, so SCREENS_INDEX rows map 1:1.
2. `tools/convert_data.py`: `.BAS` numeric arrays, INFO/ENC/MISSION text files, NAME/CHARNAME -> `game/assets/data/*.json` using the formats in DATA_FILES.md; `tools/gmap.py`: CROSSREF.md §2 tables -> `state/gmap.json`.
3. `tools/font/`: the chosen 8x8 font to `assets/font8x8.json` with its licence file.
Originals are never modified; the pipeline reads `<targets>\starcommand\starcoma\`.

## 4. Screen list in module order (ids from SCREENS_INDEX.md)
| order | module (JS) | screens | notes |
|---|---|---|---|
| 1 | `modules/startup.js` | CM-01, SU-01..SU-05 | title picture + 4-frame animation, music, main menu, new-game reset of A(), drive menu (fixed to hard disk) |
| 2 | `modules/starport.js` | PT-* (13 services) | first playable screen after the menu |
| 3 | `modules/space.js` | SP-* (14 screens/flows) | galaxy/sector scans, computer, repair, heal, inspect, equip, encounters, docking |
| 4 | `modules/inside.js` | IN-* | station/unique-area interiors, IN-n/INMAP-n persistence, atmosphere check |
| 5 | `modules/spbattle.js` | SB-* | space battle, boarding -> PLBATTLE |
| 6 | `modules/plbattle.js` | PB-* | the only 16-colour (SCREEN 7) module; terrain 1..3 / 10 / 11 |
Each module file lists its screen ids at the top; a `?screen=<id>` dev query jumps straight to a screen with a fixture `G!()` for acceptance screenshots.

## 5. Acceptance (SC-1 = B), `ACCEPTANCE.md`
One row per screen id: DOSBox reference screenshot (the owner/coordinator capture, `acceptance/ref/<id>.png`), engine screenshot (`acceptance/out/<id>.png` from the dev jump page), checklist = same text at the same row/col, same sprites at the same positions and verbs, same keys and transitions, timing within tolerance; colour differences are expected (enhancement) and listed, geometry differences are defects. A screen passes when the build lane and a reviewer lane (GLM) both tick it.

## 6. Lanes (phase 2, Opus unless noted; max 6 incl. Foreman; one owner per file; requests via STATUS.md notes as in phase 1)
| lane | model | owns | starts |
|---|---|---|---|
| build-engine | Opus | `game/engine/*`, `game/index.html`, `tools/build_atlas.py`, `tools/convert_data.py`, `game/assets/*` | at gate; blocking for the others (first milestone: display+text+sprites+input demo page showing SU-03 and a PUT test) |
| build-startup | Opus | `game/modules/startup.js` | after the engine demo milestone |
| build-starport | Opus | `game/modules/starport.js` | with build-startup |
| build-space | Opus (Fable if the SPACE flows prove too deep) | `game/modules/space.js` | after startup/starport |
| build-inside, build-spbattle, build-plbattle | Opus | their module files | sequentially as panes free up |
| build-qa | GLM | `ACCEPTANCE.md`, `acceptance/out/*` | from the first module milestone; re-runs per module |
Engine changes a module lane needs = `engine request:` note at the top of STATUS.md; build-engine applies and posts `engine done`. Commit after each milestone; STATUS.md blocks as before.

## 7. Risks / open points
- Manual vs binary (2026-10-16): the build follows the binary wherever the manual disagrees (60 rows in decode/docs/MANUAL_XCHECK.md); copy-protection check kept as shipped (length-only). the owner can reverse either by ruling.
- Input (the owner 2026-10-16): the original is keyboard-controlled; v1 input = keyboard + the gamepad mapping already built. Mouse/touch control is a probable LATER post-acceptance enhancement: not built now, but `input.js` stays structured so a pointer layer (click on a menu letter or a map cell -> injected key code) can be added without touching module code.
- Font: no original font data in the decode (it is the CGA/EGA ROM font); an open 8x8 CGA-compatible font is used, licence recorded. Not a fidelity risk under SC-1 = B.
- CGA-only sprites (banks with `.BAS` but no `.EGA` twin): rendered through the module's EGA palette remap; listed in `game/ASSETS.md`.
- MBF <-> IEEE conversion must be exact for save compatibility (test: round-trip the shipped CHARINFO.BAS byte-identically).
- Timing constants from STARTUP's calibration are replaced by fixed delays; tune against DOSBox during acceptance.
- Remaining decode unknowns with behavioural impact are listed in CROSSREF.md §5; each is referenced from the module lane's assignment so the lane reproduces the observed behaviour, not a guess.
