# Lane: mod-<MODULE> — BASIC-style pseudocode for one module

Read FOREMAN.md and `decode/brun30/RT_LEDGER.md` first. Input: `decode/listings/<MODULE>.lst` (regenerated after rt-naming), `decode/data/MODULE_CONSTANTS.md`. Output: `decode/pseudo/<MODULE>.bas.md` and `decode/pseudo/<MODULE>_SCREENS.md`.

Rules: labels = code offsets (`L_0040:`); render each runtime-call pattern as the BASIC statement it implements (e.g. `mov bx,20; RT3E_42; mov bx,2; RT3E_44; RT3F_BC; mov bx,0xaa94; RT3F_6A; RT3E_79` -> `LOCATE 20,2: PRINT S_AA94$`). Name variables by evidence only (`S_AA94$` until a literal/usage proves a meaning, then `ShipName$ 'was S_AA94$`). Near `call`/`ret` inside the module = GOSUB/RETURN or compiled subroutines; `jmp` = GOTO; conditional jumps after FCMP/FTEST = IF. Keep a `## Unknowns` section listing every runtime call you could not render. Keep a `## Variables` table (address, type, inferred name, evidence). Screens: for each distinct screen the player sees, list the LOCATE/PRINT text, the sprites PUT, the keys read, and transitions.
Commit; 5-line status to STATUS.md.

## Shared-file rule (2026-10-15, the coordinator flag)
- `decode/pseudo/tools/qb2bas.py` has ONE owner lane at a time (named in STATUS.md / FOREMAN_MEMORY.md). Non-owners request changes with a `qb2bas request:` note at the top of STATUS.md and rerun after the owner posts `qb2bas done`.

## Shell rule (the coordinator 2026-10-15)
- Claude Code blocks `rm` on a variable path (`rm -f "$S/$g"`) with a confirmation that auto-denies after ~2 min, even in bypass mode. Write rm paths as `"${S:?}/${g:?}.ext"` or as literal paths.
