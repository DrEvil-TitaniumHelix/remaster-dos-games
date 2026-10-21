# Lane: por-draft-<area> (codex) — first-draft Pascal-style pseudocode for one engine area

Read FOREMAN.md, decode/LAYOUT.md, decode/listings/INDEX.md, decode/rt/RT_LEDGER.md (runtime names; may still grow, re-read it), decode/ecl/ECL_VM.md if present.
Input: the listings of the units named in your prompt (`decode/listings/<unit>.lst` + `.c`).
Output: ONLY `decode/pseudo/<AREA>.draft.md`. Do not edit any other file.

Format:
- One section per routine: `### <unit>:<off> <Name or FUN_xxxx> (conf H/M/L)`; header line with params/locals (BP offsets), callers, callees.
- Body = Pascal-style pseudocode (`procedure`/`function`, `if/then/else`, `while`, `for`, `case`), one line per source-level statement; keep the code offset of each statement as a trailing comment `{ 2F00:01A3 }`.
- Runtime calls rendered as the Pascal they implement (`WriteLn`, string concat, `Copy`, set ops, `Random`, file I/O) using RT_LEDGER names; unknown ones stay `RT_<seg>_<off>(args)`.
- Names by evidence only: string literals shown, globals as `g_<DSoffset>` until usage proves a meaning (then `PartyCount {was g_1A2C}`), with confidence.
- End with `## Screens` (every text/menu shown: strings, positions, keys accepted), `## Globals` (DS offset, type, inferred name, evidence), `## Unknowns` (counts).
Write files as UTF-8 (PowerShell: -Encoding utf8). When done: `git add decode/pseudo/<AREA>.draft.md`, commit `por-draft-<area>: first draft`, put a 5-line block in STATUS.md directly below the title lines (never above the title), commit, reply DONE. Shell: never `rm -f "$S/$g"`.
