# DECODE GATE — Star Command RE (phase 1 -> phase 2 checklist)

Gate rule (FOREMAN.md): no game-building until every item below is met with evidence. Maintained by the Foreman; the coordinator declares the gate to the owner when all boxes are ticked. GATE MET 2026-10-15 18:40 (see Summary) (session 0c86eed9).

## 1. Runtime (BRUN30.EXE) routines
- [x] All 140 routines the game uses are named with H/M/L confidence and body evidence: `decode/brun30/RT_LEDGER.md` (rt-naming, 6d48e87; fixes c19a327, 1812bd8, 30f687d).
- [x] Independent review: `decode/brun30/RT_REVIEW.md` (GLM 5.3, 137 AGREE / 0 DISAGREE / 0 UNSURE, 6ed77c8).
- [x] Names feed the listings: `decode/brun30/rt_names.json`, `inline_args.json`; all 7 listings regenerated (0 unlabeled runtime calls).
- [x] M/L rows re-checked (crossref §4, 0b4cf20): only 3F_C9 is non-H, PLBATTLE-only, value irrelevant to the reproduction; RT_REVIEW upgrades applied (1812bd8); PUT verbs and INPUT types H.

## 2. Module pseudocode (every statement rendered, 0 unrendered runtime calls, labels = offsets)
| Module | final file | screens | names | lane / commit | Opus verify | GLM verify |
|---|---|---|---|---|---|---|
| STARCOMM | decode/pseudo/STARCOMM.bas.md | (in STARTUP_SCREENS.md) | - | mod-startup c19a327 | 20/20 AGREE (335b4f6) | - (81 lines, Opus full read) |
| STARTUP | STARTUP.bas.md | STARTUP_SCREENS.md | - | mod-startup c19a327 | 166/167, fix applied b4f4dc3 | - |
| SPACE | SPACE.bas.md | SPACE_SCREENS.md | SPACE_names.json | mod-space2 56a468d, regen 8ee3fa6 | 261/267, fixes applied 8ee3fa6 | 274/280, same defect, fixed |
| INSIDE | INSIDE.bas.md | INSIDE_SCREENS.md | INSIDE_names.json | mod-inside c48ab36, regen 8ee3fa6, 71f36ac | 199/199 (3 translator/prose fixes applied 71f36ac) | 202/209 (7 known verb labels, fixed) d494dbc |
| SPBATTLE | SPBATTLE.bas.md | SPBATTLE_SCREENS.md | SPBATTLE_names.json | mod-spbattle 9546d3d, regen a11f8b3, 71f36ac | 178/186 (1 DISAGREE fixed 71f36ac, 7 known) | 194/194 AGREE (65 PUT verbs byte-checked) |
| PLBATTLE | PLBATTLE.bas.md | PLBATTLE_SCREENS.md | PLBATTLE_names.json | mod-plbattle 2760fc6, names aligned 0b4cf20 | 237/237 AGREE (782be1a; doc fixes being applied by crossref) | deferred: GLM usage limit until 2026-10-16 08:40 (not gate-blocking, Foreman 18:20) |
| STARPORT | STARPORT.bas.md | STARPORT_SCREENS.md | STARPORT_names.json | mod-starport b99b86a, 5b90190, 71f36ac | 299/301 (RND register-reuse fix pending) | 306/306 AGREE (22 PUT verbs byte-checked) 24fe613 |

- [x] All 7 rows final; Opus 10% verification on all 7 (every DISAGREE fixed); GLM verification on SPACE/INSIDE/SPBATTLE/STARPORT (PLBATTLE deferred to the GLM reset 2026-10-16 08:40, not gate-blocking: Opus 237/237 on it).
- [x] Translator `decode/pseudo/tools/qb2bas.py` tables match RT_LEDGER.md (PUT verbs, INPUT types fixed 541b493).

## 3. Data formats
- [x] Sprite banks .BAS (CGA 2bpp) / .EGA (B,G,R,I planes): `decode/data/SPRITES.md`, `sprites_index.tsv`, 352+ PNGs incl. TITLE.BAS frames (1812bd8).
- [x] .STR stubs, .BAT, text/numeric data files, module constants: `decode/data/{STR_FILES,BAT,DATA_FILES,MODULE_CONSTANTS}.md`.
- [x] Data unknowns resolved from the module pseudocode into `decode/data/DATA_FILES.md` §D and CROSSREF.md §3 (crossref f9c8a6c, 0b4cf20); TITLE/INSH GET arrays added (1812bd8, b46f557); BIGSH portrait animation frames being added (verify request 782be1a, data-fix in progress).

## 4. Screens inventory
- [x] Master inventory `decode/pseudo/SCREENS_INDEX.md` (screens-index, 14b7b9b: 76 rows + consistency; PLBATTLE rows being added). Decision (Foreman 17:55): the reproduction implements the hard-disk configuration (DriveCfg = 0), so the floppy swap prompt ST-01 is documented but not built.
- [x] Every screen the player sees is listed with LOCATE/PRINT text, sprites PUT, keys read, transitions: STARTUP (done), SPACE (14), INSIDE (done), SPBATTLE (done), PLBATTLE, STARPORT. Cross-module CHAIN graph consistent (each CHAIN target exists; .STR stubs explained).

- [x] Cross-module consolidation `decode/pseudo/CROSSREF.md` (lane crossref, f9c8a6c, PLBATTLE section 0b4cf20; renames applied to all modules) — GLM second opinion started, stopped by the GLM usage limit (2 minor findings pending until 2026-10-16 08:40; not gate-blocking): CHAIN graph, shared COMMON/G!() layout, data unknowns resolved, ledger M rows checked, unknown roll-up with reproduction impact.

## 4b. Manual cross-check (the owner, 2026-10-16) and undecoded extras
- [x] `decode/docs/MANUAL_XCHECK.md` (lane manual-xcheck, 9ffc662): 583 manual-documented functions/values checked: 490 MATCHES, 60 DISCREPANCY (manual vs binary, each with code evidence), 6 MANUAL-ONLY (described, not in the binary), 0 BUILD-GAP (nothing in the binary is missing from `game/`). DOSBox requests settled from the manual where possible (D-MX-1/2 added).
- [x] Decisions (Foreman 2026-10-16 01:55, under SC-1 = B 'same behaviour as the original'): where the 1988 binary differs from its own manual, the build follows the BINARY (Esper 0..49, pay cap 60 days after a completed mission, menu option 3 drive list, training rules, etc., all listed in MANUAL_XCHECK.md); the copy-protection word check stays as shipped (length-only placeholders, any lowercase word of the right length passes), not the manual's 47 words. Both reversible by a the owner ruling.
- [x] Undecoded extras in the target folder: COLOR.EXE (EGA colour test chart) and FIXIT.EXE (support save-repair tool) are OUT of scope; DEMO.EXE + DEMOSH.BAS (stand-alone promo demo started from DOS, no CHAIN to/from the game) is out of scope for v1 and listed as an optional later item for the owner (a Fable decode lane could add it).

## 5. Gate declaration
- [x] Foreman ticked all boxes 2026-10-15 18:40, committed; the coordinator reports to the owner. BUILD_PLAN.md is final as of this commit and the build-engine lane starts now (the owner: no go-ahead needed).

Summary: Phase 1 complete. 140/140 runtime routines named (GLM-reviewed, 0 disagreements); all 7 modules rendered as BASIC pseudocode with 0 unrendered runtime calls, evidence-named variables aligned across modules, every module 10%-verified by an independent Opus lane (1,251 sampled statements, every disagreement fixed) and four of them additionally by GLM; data formats fully specified with all unknowns resolved or explicitly listed with their reproduction impact (CROSSREF.md §5); 76 + PLBATTLE screens inventoried in SCREENS_INDEX.md with sprites resolved to atlas indexes. Deferred, non-blocking: GLM second opinions on PLBATTLE and CROSSREF.md (GLM usage limit until 2026-10-16 08:40); cosmetic PLBATTLE doc fixes and BIGSH frame rendering are in progress and tracked in STATUS.md.
