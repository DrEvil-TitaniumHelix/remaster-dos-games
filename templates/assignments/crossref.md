# Lane: crossref (Fable) — cross-module consolidation for the decode gate

Read FOREMAN.md and DECODE_GATE.md first. Inputs: all final pseudocode (`decode/pseudo/{STARCOMM,STARTUP,SPACE,INSIDE,SPBATTLE,STARPORT}.bas.md`, PLBATTLE when its lane finishes), the `_SCREENS.md` and `_names.json` files, `decode/data/*.md`, `decode/brun30/RT_LEDGER.md`.

Output `decode/pseudo/CROSSREF.md` with evidence (offsets) for each claim:
1. **CHAIN graph**: every CHAIN site in every module (offset, target file, condition), every .STR stub, the drive-prefix logic; one diagram/table; confirm every target exists on disk and every module is reachable from STARCOMM.
2. **Shared state**: the COMMON block / `G!()` and `A()` layouts and the string arrays as used by ALL modules: one table index -> meaning, with the module+offset that proves each entry; conflicts between modules' interpretations resolved or marked unknown. Align the `_names.json` names across modules (same address = same name); list renames needed per module as `crossref rename request: <MOD> <addr> <old> -> <new>` lines at the top of STATUS.md (do not edit other lanes' files).
3. **Data unknowns**: go through the "Unknowns left" of `decode/data/DATA_FILES.md` / the data STATUS block (DATA-block count word and block A, ENC*/MISSION integer columns, IN-n array dimensions, TR-/BIGSH- name construction, CGA palette choice) and resolve each from the module pseudocode where it reads the file; write the resolution into `decode/data/DATA_FILES.md` (you own that file now) or mark it unknown with what was tried.
4. **Ledger M rows**: for every M/L row in RT_LEDGER.md, state whether any module depends on the uncertain detail (cite the site) and, if the module evidence settles it, propose the H row text as `ledger request:` lines in STATUS.md.
5. **Unknown roll-up**: the union of every module's `## Unknowns` section, deduplicated, each with its impact on a faithful reproduction (none / cosmetic / behavioural).

Commit only your files (`git add decode/pseudo/CROSSREF.md decode/data/DATA_FILES.md herdr/assignments/crossref.md STATUS.md && git commit -m "crossref: ..."`); 5-line DONE block at the top of STATUS.md.
