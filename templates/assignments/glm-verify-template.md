# Lane: glm-verify-<MODULE> (GLM 5.3) — independent verification of one module's final pseudocode

Read FOREMAN.md first (methodology: evidence with provenance, no invented names). Inputs: `decode/pseudo/<MODULE>.bas.md` (final, by a Fable mod lane), `decode/pseudo/<MODULE>_SCREENS.md`, `decode/pseudo/<MODULE>_names.json`, the listing `decode/listings/<MODULE>.lst`, `decode/brun30/RT_LEDGER.md`, `decode/data/MODULE_CONSTANTS.md`.

Task: pick 10% of the statements of `<MODULE>.bas.md` at random (seeded, list the seed) plus every CHAIN/BLOAD/ON GOTO/INPUT site, and re-derive each one from the listing bytes. For each: AGREE / DISAGREE (with the statement you derive) / UNSURE, with the listing offset and the instruction bytes you relied on. Also check: every variable name in `<MODULE>_names.json` has a `_why` that the listing supports; every screen in `_SCREENS.md` has the LOCATE/PRINT text that the string table proves; the `## Unknowns` section is honest (nothing unrendered is hidden).

Output: `decode/pseudo/<MODULE>_GLMVERIFY.md` with a verdict table, a disagreements section, and a 3-line summary (counts). Do not edit the lane's files; disagreements go into your report and into a 5-line STATUS.md block at the top. Commit only your two files (`git add decode/pseudo/<MODULE>_GLMVERIFY.md STATUS.md && git commit -m "glm-verify-<mod>: ..."`).
