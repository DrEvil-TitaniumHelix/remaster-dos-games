# Lane: por-build-ecl (Opus) — the ECL VM in JavaScript, then the VIEW area

Read BUILD_PLAN.md, FOREMAN.md, decode/ecl/ECL_VM.md, decode/pseudo/ECL.pas.md (+ ECL_SCREENS.md), decode/ecl/scripts/INDEX.md, decode/tools/ecldis.py, decode/GLOBALS.md, decode/CROSSREF.md §3/§4.

You own: game/engine/ecl.js, game/areas/ecl_*.js if you split helpers, game/test/ecl/* (node tests), later game/areas/view.js.

Milestones (commit each, `por-build-ecl: M<n> <what>`; STATUS block directly below the title lines after each):
- M1 (no engine needed): ecl.js = LoadEclBlock, operand decoder (types 00/01/02/03/80/81, packed 6-bit strings), the 4 memory regions + specials of ecl_GetMem/ecl_SetMem, gosub list, compare flags, IF-skip (ecl_SkipInstruction table), all 61 opcode handlers as in ECL.pas.md, event vectors + the engine entry points (ecl_Run loop, stop/party-dead). Opcodes that need the engine (text, menus, pictures, combat, shops) call an injected `host` interface. Node test harness: load each of the 29 ECL records from the original ECL*.DAX (dax decode can reuse decode/tools/dax.py output or a small JS dax reader until build-engine's dax.js lands), run every entry vector with a scripted host, assert the instruction trace matches ecldis.py's decoding (same PC sequence for straight-line paths, 0 undecodable ops).
- M2: bind `host` to the real engine API (engine requests to build-engine), first script on screen: the Phlan town entry (ECL1 per scripts/INDEX.md) with its texts in the text window, compared with a DOSBox reference capture (ask por-dosbox-ref via `ref request #n` in STATUS.md).
- M3: when DECODE_GATE.md / STATUS shows VIEW verified (por-verify2 VIEW_VERIFY.md with its fix requests applied): game/areas/view.js (movement, doors, explore commands, area map, encounter hand-off) from VIEW.pas.md.
Rules: translate from the verified pseudocode, keep `// seg:off` per function; unknowns as TODO(decode). Never modify or commit originals. Shell: never `rm -f "$S/$g"`; no background polling loops. `git add` only your files.
