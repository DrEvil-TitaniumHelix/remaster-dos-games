# BUILD PLAN — Pool of Radiance reproduction (phase 2)

Status: **ACTIVE 2026-10-16 11:50 MDT** — the owner (via the coordinator, STATUS.md "BUILD THE GAME NOW" block): build now, in parallel with the open gate items; engine + ECL VM lanes start immediately, area translation lanes once their area's verification has passed (fix first if it fails). Goal: a playable build tonight with a Desktop shortcut. Not clean-room (the owner 2026-10-16): verified pseudocode is translated directly, the original data files are used.

## 1. What is being built
A zero-install HTML5 game in `game/`: `index.html` + vanilla ES modules, no build step, served by `python -I tools/serve.py` (file:// blocks ES modules), Chrome on the handheld PC. EGA 320x200 16 colours, integer-scaled, nearest-neighbour. Keyboard + Gamepad API + mouse. Everything is driven by the decode: `decode/pseudo/SCREENS_INDEX.md` (screen ids), the six area files `decode/pseudo/<AREA>.pas.md`, `decode/ecl/ECL_VM.md`, `decode/CROSSREF.md` (globals, call graph), `decode/data/*.md` (formats).

**Data at runtime = the original files, read in place.** `tools/serve.py` serves `game/` and maps the URL prefix `/data/` read-only (GET only) to `<targets>\goldbox\por\POOLRAD\` (overridable by env `POR_DATA`); originals are never modified or committed. Saves go to the browser file store, never into the original SAVE/ (shipped saves are imported read-only). The engine decodes DAX records itself (JS port of `decode/tools/dax.py` + `daxpic.py`), and the ECL VM runs the original ECL*.DAX bytecode. Nothing from the data files is baked into code. This means the reproduction plays the original scripts, so content fidelity follows from VM fidelity.

## 2. Engine architecture (`game/engine/`, one ES module each)
| module | responsibility | decode source |
|---|---|---|
| `display.js` | 320x200 4-bit index framebuffer, EGA palette, canvas scaling; CGA path not built (POOL.CFG = EGA) | ENGINE.pas.md video unit 08AE, PICTURES.md |
| `dax.js` | DAX directory + RLE decode (0x7F/0x80 behaviour as the engine) | DAX.md, 0802:0716/050F |
| `pictures.js` | P/A/F records, XOR-delta animations, 8x8 symbol sets, 24x24 tiles, wall sets, portraits; blits with the engine's transparency rules | PICTURES.md, WALLDEF.md, VIEW.pas.md ov28/ov32/ov34 |
| `text.js` | text windows, word-wrapped print `(x1,y1,x2,y2,colour,clear,s)`, text cursor, the game's own font from the F records, frame drawing from symbol glyphs (#ref-3) | ENGINE.pas.md 0709, ECL_SCREENS.md |
| `input.js` | key queue with the scan/ASCII codes the menus switch on, keypad table DS:288C, menu timeouts; Gamepad API (d-pad = arrows/menu cursor, A = Enter, B = Esc, X/Y = menu letters by position); mouse = click on a menu letter or map cell -> injected key (pointer layer, no module code changes) | VIEW.pas.md ov25 menus |
| `tp.js` | Turbo Pascal semantics the code depends on: `Random` (TP 6.0 LCG RandSeed*08088405h+1, exact, seedable for acceptance runs), integer wrap/byte truncation, Pascal strings (length byte, 255 max), sets | RT_LEDGER.md |
| `ecl.js` | the ECL VM: operand decoder, 4 memory regions, gosub list, compare flags, all 61 opcodes, event vectors, the engine entry points | ECL_VM.md, ECL.pas.md |
| `state.js` | DS globals as a typed view with names from `decode/names/globals.json` (generated `state/globals.json`), party/char records in the original 285-byte TChar layout, items 63 B, effects 9 B | GLOBALS.md, CROSSREF §3, SAVES.md |
| `files.js` | save/load in the original SAVE/ formats (CHRDAT*.SAV/.ITM/.SPC, SAVGAM*.DAT) on a browser file store (IndexedDB, try/catch fallback to memory), import of the shipped saves | SAVES.md, PARTY.pas.md ov17 |
| `timer.js` | delays/menu timeouts in the original tick units, frame scheduler | ENGINE.pas.md |
| `audio.js` | PC-speaker sounds as the code emits them (Web Audio square wave); sound off flag from POOL.CFG | ENGINE.pas.md |

Areas are written as async JS over an awaitable engine API (`await input.key()`), one file per area, routine by routine with the `{ seg:off }` address of each pseudo routine kept as a comment, so every JS line traces back to evidence: `game/areas/{engine,view,party,combat,magic}.js` (+ `ecl.js` above). Copy protection: bypassed by default (as `STING`), `?wheel=1` shows the code-wheel screen PARTY-ov02-01 for acceptance shots.

## 3. Asset pipeline
Only `tools/gen_globals.py` (names json -> `game/state/globals.json`). No atlas: pictures are decoded at runtime from the DAX files. A later art pass, if wanted, would hook in `pictures.js` (picture record -> override PNG with scale factor), deferred.

## 3b. Launcher (as Star Command)
`Play Pool of Radiance.cmd` in the repo root: starts `python -I tools/serve.py 8089` minimised if the port is not already listening, then opens Chrome as an app window (`--app=http://localhost:8089/index.html`); `Play Pool of Radiance.lnk` on `<Desktop>\` pointing at it (model: StarCommandRE `Play Star Command.cmd` + its .lnk). Owner: build-engine; created at M1 so the owner can watch progress.

## 4. Build order (screen ids from SCREENS_INDEX.md)
1. engine core: display, dax, pictures, text, input, tp, timer -> milestone M1 = title sequence (TITLE.DAX records) pixel-identical to REF-TITLE-1/2 and the start menu.
2. party: top menu, character creation, roster, load shipped party (REF-MENU, REF-PARTY), training, save/load.
3. view + ecl: 3D view, area map, movement, doors, the ECL VM running ECL1..8 (town of Phlan first), text windows, shops/temples via scripts.
4. magic/camp: encamp, memorize, scribe, rest, cast outside combat.
5. combat: battlefield, deployment, round loop, player menu, monster AI, effects, treasure.
6. integration runs: new game -> first fight -> camp -> save -> reload; shipped save -> slums.

## 5. Acceptance (`ACCEPTANCE.md`)
One row per SCREENS_INDEX id: build screenshot (headless Chrome, `acceptance/out/<id>.png`), DOSBox-X reference (`acceptance/ref/<id>.png` from the por-dosbox-ref harness), `acceptance/ref/compare.py` exact-RGB diff at 320x200. Target = 0 differing pixels for static screens; for screens with random/time content the row states what may differ. A "finding about the original" is valid only when confirmed in DOSBox (SC lesson). Behavioural scenario runs with a fixed `tp.js` RandSeed are compared against DOSBox runs with the same key script where feasible.

## 6. Lanes (phase 2; max 6 panes incl. Foreman; Opus finals, codex for JS first drafts of large areas)
build-engine (Opus, owner of game/engine/ except ecl.js, plus tools/serve.py and the launcher), build-ecl (Opus: game/engine/ecl.js, then game/areas/view.js once VIEW verifies), build-party (Opus), build-combat (codex draft -> Opus), build-magic (codex draft -> Opus), por-dosbox-ref (codex, references + compare for every id), build-qa (Opus: ACCEPTANCE.md, integration runs). Requests between lanes via tagged STATUS notes (`engine request #n` / `engine done #n`).

## 7. Risks / open points
- Timing: the original's delays are CPU-speed-bound in places; use the DOSBox cycles value of the reference harness as the yardstick.
- Mouse: the original has no mouse support (to verify in ENGINE input code); mouse is an added pointer layer -> keys, not a behaviour change.
- Random-dependent screens need seeded comparisons, not single shots.
