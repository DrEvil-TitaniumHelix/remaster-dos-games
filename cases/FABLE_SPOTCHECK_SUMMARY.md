# Independent spot-check of an Opus-only decode (Pool of Radiance, 2026-10-16)

A bounded Fable lane (about one hour, about 1% of a weekly budget) re-read a seed-fixed random sample of the Opus/codex decode directly from the disassembly, wrote its own account of each item first, then compared.

- Routine totals: **27 AGREE / 1 MINOR / 2 WRONG** (both WRONGs are local: one misplaced branch, one reversed call).
- Opcode totals: **7 AGREE / 1 MINOR / 0 WRONG**.
- Hard-spot totals: **3 AGREE** (plus AttackRollVsAC as a bonus, AGREE).
- Estimated fidelity: **90 % of routines are statement-for-statement correct, 93 % correct or only cosmetically off**

Both wrong items were call-shape errors (a parameter list written in reverse push order, a branch attached to the wrong test); no wrong formula, offset or constant was found.

Where not to trust a decode blindly (now rules in METHOD.md):
1. Calls annotated with a push-order comment: re-check against the callee's declaration.
2. Prose sketches of menu loops: the extended-key / plain-key split and exact colours are where drafts skimp.
3. Index bases in table comments: prefer the data-format spec.
4. Very large routines written by forked workers: only sampled.
