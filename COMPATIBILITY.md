# COMPATIBILITY — which original toolchains the method is known to work on

Each row links to a profile in `profiles/`. Status levels, lowest to highest:

| Level | Meaning |
|---|---|
| untested | nobody has tried it; listed so contributors can claim it |
| gate-passed | Phase 0 gate test passed on at least one real game (code readable, one layer found, decompiles coherent) |
| decoded | a full decode gate was met on at least one game |
| playable | a rebuild of at least one game is playable end to end |
| oracle-verified | that rebuild matches the original screen by screen against an emulator reference |

| Toolchain / runtime | Typical era and games | Status | Proven on | Profile |
|---|---|---|---|---|
| Microsoft QuickBASIC 3 (BRUN30) | 1987-88 hobby and small-publisher games | **oracle-verified** | Star Command (SSI 1988) | `profiles/quickbasic-3` |
| Turbo Pascal 6 + FBOV overlays (+ EXEPACK) | 1988-91, SSI Gold Box | **decoded**, alpha build released (69 of 105 screens match the original at 0 px; all 29 script areas play; overland map and endgame not verified, so not yet "playable end to end") | Pool of Radiance (SSI 1988) | `profiles/turbo-pascal-6` |
| Microsoft C 6 + PKWARE-imploded overlays | 1990-92 | **decoded** (partial: overlay extraction and Ghidra export proven, most areas decoded, no build) | Darklands (MicroProse 1992) | `profiles/microsoft-c-6` |
| Script / bytecode VMs (game-specific) | many adventure and RPG engines | gate-passed via the ECL VM inside Pool of Radiance | Pool of Radiance ECL | see turbo-pascal-6 |
| QuickBASIC 4.x / BASIC PDS 7 | 1988-92 | untested | | |
| Turbo Pascal 5.x / 7.0, Borland Pascal | 1988-93 | untested (expected close to TP6) | | |
| Turbo C / Borland C++ (optimisations off) | 1988-93 | untested | | |
| Microsoft C 5.x / 7.x, Visual C++ 1.x (16-bit) | 1988-94 | untested | | |
| Watcom C/C++ (DOS/4GW, 32-bit, optimising) | 1993-97 | untested, **expected hard** (optimising compiler + protected mode) | | |
| Clipper / dBase-compiled | business-style games | untested | | |
| Hand-written x86 assembly engines | action games, 3D engines | untested, **expected hard** (no source statements to recover) | | |
| SCUMM / SCI / AGI | LucasArts, Sierra | out of scope: ScummVM already reimplements these | | |

Add a row by pull request (see CONTRIBUTING.md). A status only moves up with evidence in the profile.
