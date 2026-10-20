# PROFILE — Microsoft C 6 with a custom overlay scheme (PKWARE-imploded overlays)

Status: **reproduced** (Darklands+, bouchacha, MIT, October 2026: static recompilation to C, native build, verified on our own copy 2026-10-19). Our own decode-first attempts: partial, no build.
Proven on: Darklands (MicroProse, 1992)

## Identification
- Resident EXE of about 64 KB with the overlays appended; a resident directory table locates them (in this game at resident offset 0x0BF7E, 81 overlays).

## Packing and overlays
- Overlays are compressed with PKWARE DCL implode (1.02). Static extraction: parse the directory, decompress each overlay, load it into Ghidra at its own load segment.
- A dynamic route (running the game and recording executed code) reached only about 21% coverage on this game in an earlier attempt: use the static route.

## The one layer
- No language runtime layer of the QuickBASIC kind; the overlay directory plus the resident core play that role. Large decode areas: combat, location builders, city screens.

## Decompile notes
- MS C 6 at the settings used decompiles well in Ghidra after the overlays are extracted.
- REA (a multi-tool reverse-engineering front end) sees only the 59 KB resident image and its raw-binary x86 mode is 32-bit; it is not usable for the overlays.

## Results so far
- Export of the resident core plus 81 overlays (about 4,400 functions, about 86% of bytes) done in under 20 minutes; most areas decoded and partly verified, then work was stopped by choice. No build attempted by us.
- Darklands+ (bouchacha, MIT, October 2026) then reproduced the whole game by the METHOD revision-2 route: every function statically recompiled to C over a flat emulated real-mode memory (RTLink overlays and EMS emulated in the runtime), native SDL build, modern screens added one at a time behind hooks. Built from our own copy in under two minutes; start, battle, save and load pass. See `cases/DARKLANDS_CHALLENGE.md` and `docs/DARKLANDS_PLUS_ANALYSIS.md`.
