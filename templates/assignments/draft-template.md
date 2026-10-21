# Lane: draft-<mod> (Astra/codex) — first-draft BASIC pseudocode for one module

Read FOREMAN.md and `decode/brun30/RT_LEDGER.md` first (the ledger is being extended by another lane; re-read it when you need a routine name). Input: `decode/listings/<MODULE>.lst` plus `decode/data/MODULE_CONSTANTS.md` if it exists. Output: ONLY `decode/pseudo/<MODULE>.draft.md` (create `decode/pseudo/`). Do not edit any other file.

Format (same as the final lanes): labels = code offsets (`L_0040:`); render each runtime-call pattern as the BASIC statement it implements (e.g. `mov bx,20; RT3E_42; mov bx,2; RT3E_44; RT3F_BC; mov bx,0xaa94; RT3F_6A; RT3E_79` -> `LOCATE 20,2: PRINT S_AA94$`). Name variables by evidence only (`S_AA94$` until a literal/usage proves a meaning, then `ShipName$ 'was S_AA94$`). Near `call`/`ret` inside the module = GOSUB/RETURN or compiled subroutines; `jmp` = GOTO; conditional jumps after FCMP/FTEST = IF. Unknown runtime calls stay as `RT3x_nn(args)` with the register args shown; never invent a meaning. End with `## Unknowns` (every runtime call you could not render, with count) and `## Variables` (address, type, inferred name, evidence).
When done: `git add decode/pseudo/<MODULE>.draft.md && git commit -m "draft-<mod>: <MODULE> first draft"`, append a 5-line block to STATUS.md (commit that too), reply DONE.

## Shell rule (the coordinator 2026-10-15)
- Claude Code blocks `rm` on a variable path (`rm -f "$S/$g"`) with a confirmation that auto-denies after ~2 min, even in bypass mode. Write rm paths as `"${S:?}/${g:?}.ext"` or as literal paths.
