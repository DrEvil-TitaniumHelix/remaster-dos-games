# fable-confirm — independent Fable spot-check of the Opus decode (the owner 2026-10-16: "OK to run a Fable confirmation")

Purpose: the owner is surprised the decode worked on Opus. Give an independent, deeper-model second opinion on whether the Opus/codex pseudocode is faithful. **Fable weekly budget is at 84%; the coordinator stops it at 90%. Keep this SMALL and finish in about 1 hour.** Read-only on decode files: write only `decode/FABLE_CONFIRM.md` and a STATUS block. Do not edit pseudocode; list discrepancies for the owners.

## Sample (fixed, so the result is comparable)
1. 30 routines, chosen at random with a fixed seed (`random.seed(1988)`) across the six areas, weighted by area size: ENGINE, ECL, VIEW, COMBAT, MAGIC, PARTY (`decode/pseudo/*.pas.md` vs `decode/listings/` disassembly). For each: read the listing yourself first, write a one-paragraph independent account, then compare to the pseudocode. Verdict per routine: AGREE / MINOR (naming, wording) / WRONG (behaviour differs: say exactly where).
2. 8 ECL opcodes at random (same seed) from `decode/ecl/ECL_VM.md`: check the handler code for operand decoding and semantics.
3. The 3 hardest spots you see while sampling (e.g., combat to-hit/damage, THAC0/saving throws, spell effects): check each formula end to end against code.

## Report (`decode/FABLE_CONFIRM.md`)
Table per item (id, area, verdict, evidence offset, note), totals, estimated fidelity %, and a one-paragraph verdict for the owner: is the Opus decode trustworthy enough to build from, and where would you not trust it. Commit `fable-confirm: spot-check report`. STATUS block `fable-confirm DONE`.
