# Lane: por-tooling (Opus) — unpack, overlay layout, Ghidra project, listings

Read FOREMAN.md first (Target facts, Method). Target folder `<targets>\goldbox\por\POOLRAD\` (WSL `/mnt/<targets>/goldbox/por/POOLRAD/`). NEVER modify originals; copy what you need to `decode/bin/` (gitignored if > 1 MB; small derived files may be committed).

## Steps (commit after each, `por-tooling: <what>`)
1. `decode/tools/unexepack.py`: unpack START.EXE (Microsoft EXEPACK; backwards RLE + packed relocation table) to `decode/bin/START.unpacked.exe`. Evidence: stub signature, header fields, resulting MZ header, relocation count, entry point; the Turbo Pascal copyright string visible in the image. As soon as this works, put the line `unpacked done` at the top of STATUS.md (another lane, por-rt, waits for it) and commit.
2. Turbo Pascal overlay layout: find the overlay manager data in START.EXE (TP 5.x/6.0/7.0 `FBOV` scheme: per-unit stub segments with `CD 3F` INT 3Fh stubs, stub header = return addr / file offset / code size / fixup size / entry count ...), parse the FBOV header of GAME.OVR, and map every overlay unit to file offset, code size, fixup table, entry points and the stub segment it belongs to. Identify the TP version by evidence. Write `decode/tools/tpovl.py` and `decode/LAYOUT.md`: every code unit (resident units incl. System/CRT/DOS/Overlay and every overlay unit) with size, load segment chosen for analysis, entry stubs, data segment (DS) location and size.
3. Ghidra headless project (WSL, `wsl.exe -d Ubuntu -- bash <script>`; env per FOREMAN.md; project dir `ghidra_proj/` is gitignored): load the resident image at its segments and each overlay unit at its own distinct segment, apply the overlay fixups so far calls into stubs resolve to the target unit's routines (rewrite/label `CD 3F` stub entries as jumps to the unit + entry offset). Adapt `decode/ghidra_scripts/BrunExport.java` to an overlay-aware export: `decode/listings/<unit>.lst` (disassembly) and `decode/listings/<unit>.c` (decompile) per function, with a names-map hook (`decode/names/*.json`, address -> name) so later lanes' names flow in on regeneration. Only one Ghidra at a time on this machine.
4. Gate check for this step: pick 3 real engine functions (e.g. the one printing a known GAME.OVR string, the file-open path for a `.DAX` name, the main loop) and show they decompile sensibly; write that into LAYOUT.md `## Gate check`. Also write `decode/listings/INDEX.md` (unit, function count, address range).

## REA (the owner 2026-10-16, see FOREMAN.md Method)
- Use REA when it helps on the UNPACKED START.EXE only (strings/xrefs/procedure inventory, quick single-function decompiles, evidence bundles): WSL only, `wsl.exe -d Ubuntu -- bash <script>` with env from `~/bin/rea-mcp`, or the `rea` MCP tools if loaded. It cannot see the FBOV overlays: overlays and bulk exports stay on tpovl.py + Ghidra headless.

## Rules
- Every claim = Evidence (file, offset, bytes) or explicit unknown; confidence H/M/L.
- Shell: write rm paths as literal or `"${S:?}/${g:?}"`; never `rm -f "$S/$g"` (blocks in bypass mode). No background polling loops.
- `git add` only your own files (decode/tools/unexepack.py, tpovl.py, decode/LAYOUT.md, decode/listings/, decode/ghidra_scripts/, decode/bin small files) plus your STATUS.md block. Never `git add -A`.
- When done: STATUS.md block (newest first: lane, result, files, open questions), commit, reply DONE.
