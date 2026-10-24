# Darklands+ (bouchacha) vs our Darklands attempts

Written 2026-10-19. Source: github.com/bouchacha/Darklands-plus (MIT), cloned and built locally.

## What it is
- 329 commits, 2026-10-07 to 10-14 (7 working days). Written entirely by Claude for a non-programmer author, who has handed it over (no maintainer, forks welcome).
- Two tracks on one toolchain:
  1. **Matching decompilation.** 382 C files that MS C 6.00A compiles back to the original bytes: 84% of ~10,100 functions, and `build.py` rebuilds a byte-identical DARKLAND.EXE. A "functional" build reaches 94% C.
  2. **Darklands+ port.** A static recompiler (`port/recomp/recomp16.py`, 676 lines) turns every x86 function into a C function that runs on an emulated CPU and a flat 1.1 MB memory array. This is built on the player's machine from their own EXE. A small runtime (about 7k lines of C: DOS, BIOS, EMS, Sound Blaster/MPU-401, SDL) runs it natively with no DOSBox. Modern screens are then added through a hook chain, one screen at a time.

## How he solved overlays (the layers)
- **The overlay manager is RTLink/Plus**, not plain MS LINK. That is 136 sections, the table at segment 09C0+0B74, and 740 vector thunks. We had found the same table on 10/16 but called it MS LINK.
- **His code is native, but the bytes are still loaded.** `runtime/ovl.c` copies each section's bytes into the emulated memory and applies its relocations on demand, exactly as RTLink does. So code-segment data, patched segment values and "which sibling overlay is in memory" all stay faithful.
- **Vector calls become brackets.** Every call through a vector is translated to `ovl_save; ovl_enter(n); target(); ovl_restore`, which reproduces RTLink's reload stack. When a card script is displaced by the code it calls, it is reloaded on return. His bug note: without this, merchant travel teleported the party.
- **Address collisions:** overlays share addresses, so the dispatcher picks the function belonging to the section that is currently loaded.
- **Interrupt handlers that load overlays:** the overlay area is saved before the handler runs and put back after it. Without this, pictures came out as garbage.
- **Parent-chain rule:** a section is present only together with its whole chain of parents. Loading one section evicts the sections it overlaps and their descendants.

## How he solved memory switching (EMS)
- `runtime/ems.c` emulates LIM EMS 4.0 at a high level (int 67h). The page frame is at E000 with 4×16 KB pages, backed by 8 MB of host memory. Mapping copies pages in and out, and the whole state can be snapshotted, so "what-if" evaluations of game code roll back cleanly.
- **Memory residue comes for free.** All game state lives in one byte array laid out exactly like the original, so leftover memory between overlays behaves identically. This is the thing that sank our first (dynamic) attempt.

## Hand work he needed
- 1 override: the EMS init routine rewinds its own return address.
- 12 functions always run in a fallback interpreter: a picture decoder that is a coroutine on its own stack, and a self-modifying driver thunk.
- 13 extra entry points.

That is the entire residue of "things static translation can't express".

## Why he succeeded and we didn't

| | First attempt, dynamic (Aug–Sep 2026) | Second attempt, static (Oct 2026) | Darklands+ |
|---|---|---|---|
| Route | dynamic: coverage by playing (Spice86/BizHawk) | static: decode to pseudocode, then rewrite | static: **recompile instructions**, then replace screens |
| What must be understood before anything runs | the whole game | the whole game | **nothing.** It runs first, understanding comes per screen |
| Overlays | defeated it | extracted and exported (gate passed) | emulated exactly, like RTLink |
| Memory residue / EMS | the blocker | no answer, so we stopped | reproduced for free (same memory image) |
| Correctness check | play-testing | pixel oracle (planned) | **byte-identical rebuild** (the compiler is the oracle) + lock-step side-by-side runs + "Play original" switch |
| Result | combat in C#, 21% coverage | stopped by choice | whole game playable natively, plus QoL, in 7 days |

**Root cause:** our METHOD assumes the remake is a *rewrite from understood pseudocode*. For Star Command and Pool of Radiance that works because the logic sits on a clean layer (the BRUN runtime, the ECL VM). Darklands has no such layer. Its behaviour depends on memory layout, overlay residency and EMS state, so a rewrite must reproduce things nobody has decoded. He sidestepped this: he translated *instructions*, not *meaning*, which keeps every side effect, and only then took the game apart module by module. Each step stays playable and can be compared against the original.

Second cause: the matching-decompilation track gives a mechanical, countable proof (bytes equal or not). Our gate relied on readable pseudocode, which cannot prove absence of divergence.

## What to integrate into Remaster DOS Games (proposal)
1. **METHOD.md: add Route B "recompile, then replace"**, alongside Route A "decode, then rewrite".
   - Choose B when no clean layer exists (R3 fails) or behaviour depends on memory residue, overlays or EMS. This turns today's disqualifier D2 into a route switch.
   - Phases for B: (0) overlay manager and section table parsed, (1) recompile and run with no DOSBox, (2) "Play original" switch plus a lock-step oracle, (3) native screens via hooks, one at a time, each with an on/off comparison.
2. **Credit and reference rather than copy.** Link Darklands+ from CASES.md as the Darklands case, done by someone else with this route. It is MIT, so reuse with attribution is allowed.
3. **Generic tool (later, optional):** turn `recomp16.py` + `ovl.c` + `ems.c` into a game-agnostic `tools/recomp16/`. Today they are Darklands-specific: segment 09C0 and section 136 are hard-coded. A plug-in per overlay manager (RTLink, MS LINK, Turbo Pascal FBOV via our `tpovl.py`) would make it a real second engine path. Proof test: Pool of Radiance recompiled and running, with no DOSBox.
4. **Darklands itself:** the community-challenge framing in our README is overtaken. Darklands+ *is* the answer, and forks are invited. Options: point to it, or fork it as the maintained continuation (a separate ruling).
