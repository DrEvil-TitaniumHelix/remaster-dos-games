# Lane: por-mod-<area> (Opus) — FINAL Pascal-style pseudocode for one engine area

Read FOREMAN.md, decode/LAYOUT.md, decode/listings/INDEX.md, decode/rt/RT_LEDGER.md, decode/GLOBALS.md, decode/ecl/ECL_VM.md (if present), decode/data/INDEX.md, herdr/assignments/por-areas.md (your units). A codex draft `decode/pseudo/<AREA>.draft.md` may exist: it is a mechanical skeleton, use it only as a checklist; the listings (`decode/listings/<unit>.lst` asm = the evidence, `.c` = Ghidra help) are the source.

Outputs (you own them):
- `decode/pseudo/<AREA>.pas.md`: every routine of your units, `### <seg>:<off> <Name> (H/M/L)` + signature (params by BP offset, result), callers/callees, body = readable Pascal-style pseudocode at source level (one statement per line, `{ seg:off }` of the first instruction), runtime calls as the Pascal they implement, globals by GLOBALS.md name, ECL/data structures by their spec names. Every name with evidence; unknowns stay `FUN_`/`g_` and are listed.
- `decode/pseudo/<AREA>_SCREENS.md`: every screen/menu/message the area shows: id `<AREA>-nn`, trigger, text with row/col or window, keys accepted, picture records drawn, next screen.
- `decode/names/<area>_names.json` ({"SSSS:OOOO": "Name"} for routines; `"DS:XXXX"` for globals you name). Global names you introduce: write a `globals request #n` note in STATUS.md for por-tooling (owner of GLOBALS.md/globals.json) instead of editing those files.
- Before DONE run `python -I decode/tools/argcheck.py` on your .pas.md (see herdr/assignments/por-argcheck.md; writes decode/pseudo/<AREA>_ARGCHECK.md) and fix every MISMATCH.
- Verification at the end: re-read 10% random statements against the asm, record the sample + result in a `## Self-check` section.

Rules: Evidence or explicit unknown, confidence on every name, no invented names; the binary wins over public docs. `git add` only your files + your STATUS.md block (directly below the STATUS title lines); commit after each unit (`por-mod-<area>: <unit>`), so a lost pane loses little. Shell: never `rm -f "$S/$g"`; no background polling loops; Ghidra re-export only via a `ghidra request #n` to por-tooling. When done: STATUS block, commit, reply DONE.
