# Lane: por-ecl (Opus) — the ECL script VM ("the one layer")

Read FOREMAN.md, `decode/LAYOUT.md`, `decode/listings/INDEX.md`, `decode/rt/RT_LEDGER.md` (if present) and `decode/data/DAX.md` (ECL*.DAX at container level is por-data's; the bytecode is yours). Use `decode/tools/dax.py` (owned by por-data) to extract ECL records.

## Steps (commit after each, `por-ecl: <what>`)
1. Find the ECL interpreter in the listings: the routine that loads an ECL record, the instruction fetch loop, and the opcode dispatch table (jump table or array of near/far procedure pointers indexed by opcode). Cite address + bytes.
2. Operand encoding: how each operand is fetched (immediate byte/word, memory variable reference, string, address), including the operand-type byte scheme. Spec it with the fetch routine as evidence.
3. Every opcode: number, handler address, operand count/types, semantics in Pascal-style pseudocode from the handler body, effects on VM state (PC, compare flags, variables, stacks, game state globals), confidence H/M/L. Unknown semantics stay unknown with what is known.
4. VM state: memory/variable map the scripts address (ECL "memory" area, game globals reachable from scripts), event/trigger tables (vectors at the record start, e.g. on-move, on-search, on-rest, on-init), and how the engine calls into the VM.
5. `decode/ecl/ECL_VM.md` (spec), `decode/tools/ecldis.py` (disassembler driven by the spec), `decode/ecl/listings/ECL<n>_<rec>.ecl.txt` for every record of all 8 ECL*.DAX; table of opcode usage counts across all scripts; every opcode that appears in data must be specified (gate item).
6. Cross-check against public Gold Box ECL documentation (cross-check only, note agreements/disagreements in a section; the binary wins).

Rules: Evidence (address, bytes, routine body) or explicit unknown; you own decode/ecl/, decode/tools/ecldis.py, decode/names/ecl_names.json. `git add` only your files + your STATUS.md block. Shell: never `rm -f "$S/$g"`; no background polling loops; Ghidra only if no other lane runs it (ask in STATUS.md via `ghidra request #n` to por-tooling). When done: STATUS.md block at the top, commit, reply DONE.
