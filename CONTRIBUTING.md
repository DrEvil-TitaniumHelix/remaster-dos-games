# Contributing

The most valuable contribution is **a new toolchain profile**: you tried the method on a game built with a compiler or runtime not yet in `COMPATIBILITY.md`, and you report what happened, success or failure. Failures are welcome; they set the limits of the method.

## What a pull request may contain
- A new or updated profile under `profiles/<toolchain>/PROFILE.md` (copy `profiles/TEMPLATE.md`).
- A row change in `COMPATIBILITY.md`, raised only to the level your evidence supports.
- Tools under `tools/` (unpackers, overlay splitters, runtime-aware disassemblers, Ghidra scripts), each with a header comment saying what it does, what it was tested on, and how to run it.
- Improvements to `METHOD.md`, `SCALING.md` or `templates/`, with the reason (ideally a trap you hit).

## What a pull request must never contain
- Original game files, executables, data, or anything extracted or derived from them (unpacked binaries, ripped graphics, decoded text dumps, decompiled listings, pseudocode of copyrighted games). Profiles describe *how*, with short byte-pattern evidence, never the game's content.
- Credentials, personal paths or machine names.

## Evidence rules (same as METHOD.md)
- Every claim cites where it was observed (file, offset, a few bytes) or is marked unknown. Confidence H/M/L.
- Status levels in `COMPATIBILITY.md` move up only with evidence in the profile: a gate-test table for gate-passed, a ticked decode gate summary for decoded, a playable run for playable, emulator reference matches for oracle-verified.
- Say which models and how many lanes you used, and the hardware, so results are comparable.

## Process
1. Open an issue with the "New toolchain profile" template to claim a toolchain (avoids duplicate work).
2. Run the Phase 0 gate test from METHOD.md and fill the profile's gate table.
3. Open a pull request using the template; one toolchain per pull request.
4. A maintainer checks the evidence rules and the "never contain" list before merging.
