# Lessons from the first two runs (condensed from the Foremen's working memories)

## Star Command (QuickBASIC 3), 2026-10-15/16
- The first REA survey showed only the loader stub as code; the module header at 0x40 had to be decoded by hand before any listing existed. Lesson: the "one layer" may be invisible to generic tools; plan to build a runtime-aware disassembler on day one.
- 140 runtime routines named in one lane, with a GLM review lane checking each ledger row: naming plus independent review was the fastest path to readable listings.
- Codex drafted each module (11-17K lines in 3-10 minutes); a deeper-model lane finalised. Reusing a finished final-lane session for the next module kept its translator know-how and cut later modules to under an hour.
- Two lanes edited the same tool file and one commit swept in the other's half-finished edit: origin of the one-owner-per-shared-file rule.
- A request note was matched against an older note with the same file name and sat unanswered: origin of tagged requests (`<file> request #n`).
- A lane in bypass mode blocked on a confirm dialog for `rm -f "$VAR/..."` outside the repo; write `"${VAR:?}/..."`.
- A watcher loop inside a lane was killed for low memory; lanes do not poll, the Foreman waits.
- A usage-limit pause mid-run cost nothing because the Foreman had written a HANDOFF block; the resumed session continued from files.
- The oracle (headless DOSBox-X) arrived after playable v1 and still found three decode-error classes no review had caught.

## Pool of Radiance (Turbo Pascal 6 + overlays), 2026-10-16
- EXEPACK unpacked and the FBOV overlay layout decoded within the first hour; an overlay-aware Ghidra project (every unit at its own segment, stubs rewritten as far-jump thunks) gave 1,347 coherent functions.
- The data lane cracked the container format from the game's own loader code first; every later format (pictures, maps, monsters, saves) followed in hours. Visual review of renders caught a wrong animation assumption (frames are XOR deltas).
- The ECL script VM (61 opcodes) was the one layer; once specified, all 29 event scripts (about 16,000 statements) were verified mechanically against the disassembler.
- All areas reached final pseudocode in about 3h20 on Opus + codex with zero refusals; the build started in parallel with the last verification passes, translating an area only after its verification passed. The build itself caught further small decode errors.
- Twelve lanes across two projects saturated a 16 GB handheld (0.3 GB free, CPU 100%): origin of SCALING.md and the lane cap.
