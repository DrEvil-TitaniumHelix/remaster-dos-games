# Darklands (MicroProse, 1992): challenge fulfilled

> **Fulfilled, 2026-10-19.** [Darklands+](https://github.com/bouchacha/Darklands-plus) (bouchacha, MIT, October 2026,
> written with Claude) runs the whole game natively: a static recompiler translates every function of the player's
> own `DARKLAND.EXE` into C over an emulated CPU and a flat real-mode memory; the RTLink/Plus overlay manager
> (136 sections, not the 81-record directory described below) and LIM EMS are reproduced in a small runtime, so the
> memory residue that stopped the attempts below is reproduced for free. A second track rebuilds a byte-identical
> executable from 84% of the functions as compilable C. Hand work left: one override and twelve interpreter-only
> functions. We built it from source against our own copy in under two minutes; its smoke test (start, battle, save,
> load) passed. The rest of this page is kept as the record of why decoding alone could not finish it; its route is
> now `METHOD.md` revision 2 ("reproduce, then recode"). Credit belongs to Darklands+'s author.

Darklands was decoded in part with the revision-1 method and had **no rebuild** until Darklands+. This page lists
everything known so far that can be published: facts about the program's structure, the route that works, and the two
places where earlier attempts stalled. It contains no game material; you need your own copy, and nothing extracted
from it may be posted here (`CONTRIBUTING.md`).

## Known facts
- **Toolchain:** Microsoft C 6 (`profiles/microsoft-c-6/PROFILE.md`). At the settings the game was built with, the code
  decompiles well in Ghidra once the overlays are extracted.
- **Layout:** a resident EXE of about 64 KB with the overlays appended. A resident **overlay directory at resident offset
  0x0BF7E** locates them: **81 overlays**.
- **Packing:** the overlays are compressed with PKWARE DCL implode (1.02). Static route: parse the directory,
  decompress each overlay, load it into Ghidra at its own load segment.
- **Ghidra export: proven.** The resident core plus all 81 overlays were exported (about 4,400 functions, about 86% of
  the code bytes) in under 20 minutes. The export itself is derived from the game and is not shared; the route above
  reproduces it from your copy.
- **The one layer:** there is no language-runtime layer of the QuickBASIC kind; the overlay directory plus the resident
  core play that role. The large decode areas are combat, location builders and city screens.
- **Status of the earlier run:** most areas were decoded and partly verified, then work stopped by choice. No build was
  attempted, no acceptance screens exist, and the decode is not public.

## Where earlier attempts stalled
1. **The dynamic route.** Recording the code that runs while playing reached only about **21% code coverage**. Use the static
   route instead (`METHOD.md` principle 1: every byte of code extracted, coverage complete by construction).
2. **A tool that could not see the overlays.** A general reverse-engineering front end saw only the 59 KB resident
   image, and its raw-binary x86 mode is 32-bit, so it could not read the 16-bit overlays at all. Extract the overlays
   yourself and load each one into Ghidra as 16-bit real-mode code at its own segment.

## How to take it on
1. Run the gate test (`METHOD.md` §Phase 0) on your own copy; record your version and file sizes in your notes
   (version requirements are unknown here).
2. Follow the Microsoft C 6 profile: overlay directory, decompression, one Ghidra project with every overlay at its
   segment.
3. Split by overlay groups (combat, locations, cities, the rest), one decode lane per group plus an independent
   verifier (`ARCHITECTURE.md`, `SCALING.md`).
4. Keep your decode in **your own repository**; link it in `CASES.md` by pull request, and send what you learn about the
   toolchain to `profiles/microsoft-c-6/PROFILE.md`. Raise its level in `COMPATIBILITY.md` only with evidence.

Questions and progress reports: open an issue in this repository with the "method problem" or "new toolchain profile"
template.
