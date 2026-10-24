# METHOD — the rulebook

Revision 2 (2026-10-19). Revision 1 asked one question: *can we decode this game and write it again?* It was proven on Star Command and Pool of Radiance and failed on Darklands. Darklands+ (bouchacha, MIT, October 2026) then showed the question was wrong. Revision 2 asks two questions, in this order.

## The two questions, in order
1. **Can we reproduce it?** Translate the whole executable mechanically into code we own, running on a memory image identical to the original's, with the machine's services (DOS, BIOS, expanded memory, video, sound, the language runtime) emulated at a high level. No understanding needed. Faithful by construction, playable on the first day, and the original running in lock-step is the oracle. This is **Stage 1, Reproduce**, and it is the foundation of every remake.
2. **Can we recode it?** With the game running as thousands of named functions, replace modules one at a time, by value: a screen, a rule, a fix. Each replacement is small, has an on/off switch, and is checked against the untouched rest. Decoding is done per module, when it pays. This is **Stage 2, Recode**.

Revision 1's whole-game decode is Stage 2 applied to every module at once. It stays available for games where the code is near its source and the owner wants a runtime-free product (HTML5), but it is no longer the gate anything waits on.

## Why it works (the causes, in order of weight)
1. **Reproduce before understand.** Static recompilation turns each instruction into C over an emulated CPU and a flat real-mode memory. Everything the original does by accident (what is left in memory when an overlay is swapped out, which expanded-memory page is mapped, which overlay is resident) is reproduced, because the memory is the same. This is exactly what sank the dynamic Darklands attempt (~21% coverage) and the static decode retry (behaviour that lives in no function). Darklands+ reached a playable native game in seven days by one author and Claude; we rebuilt it from our own copy on 2026-10-19 in under two minutes and its smoke test (start, battle, save, load) passed.
2. **Static, whole-program, every byte owned.** Both stages start from a complete static analysis of the executable. Coverage is 100% by construction; nothing depends on what a player happened to exercise.
3. **The one layer tells you what is cheap to recode.** Every game has a choke point: a language runtime with a call table (Star Command: 140 BRUN30 routines), an overlay manager (Darklands: RTLink/Plus, 136 sections), a script VM (Pool of Radiance: 61 ECL opcodes). In Stage 1 it is a list of services to emulate. In Stage 2 it is the map of which modules decompile near-source and can be recoded fast.
4. **The oracle is built in.** The original and the reproduction run side by side, driven by the same script; divergences point at the runtime, not at a guess. "Play the original game" switches every recoded module off at once.
5. **Many fresh contexts, one persistent Foreman (Herdr); state in files, never in chat; independent verification before trust.** Unchanged from revision 1 and still what makes the work parallel and survivable.
6. **Recode = translation, by module.** Verified pseudocode for one module becomes native code behind a hook, with an on/off comparison. Not a redesign, and never the whole game at once.

The model is not the key ingredient: Darklands+ was written by Claude for a non-programmer; Pool of Radiance was decoded on Opus and codex with zero refusals. The route is the ingredient. REA is a first-hour survey tool only.

## The core mechanism, revised
1. **Mechanical translation needs no source-likeness.** The recompiler maps instructions, not statements. Optimising compilers, hand-written assembly and register tricks are translated the same way as naive compiler output. What it cannot express (code that switches stacks, patches its own operands, or is reached only through data pointers) falls to a small fallback interpreter; Darklands needed 12 such functions and one override out of ~10,100.
2. **The machine's services are the real work.** The runtime is the list of interrupts and hardware the game touches: DOS file and memory calls, BIOS video and keyboard, expanded memory (LIM EMS), timer, sound chips, mouse. Each is emulated at a high level once and shared by every game after the first.
3. **Overlay managers are reproduced, not reverse-engineered away.** Section bytes and relocations are loaded into the emulated memory on demand, exactly as the manager did; vector calls become save-load-call-restore brackets so a displaced caller is reloaded on return; address collisions resolve to the resident section; interrupt handlers that load sections save and restore the overlay area. (Each of these was a shipped bug in Darklands+, found by lock-step play.)
4. **Understanding is then cheap, because it is local.** A module is recoded against a running game: decompile it, build a model of its state through named accessors, draw it natively, route actions through the game's own routines, compare on and off. Turning near-source code into pseudocode is a translation task language models do well; inferring hidden logic from raw bytes or by watching play is not. Stage 2 only ever asks the first kind of question.
5. **Completeness is countable and correctness is measurable** at both stages: every function translated or interpreted; smoke and lock-step runs pass; per module, pixel comparison on and off.

## Target suitability
Status legend: **proven** = done on a real game; **expected** = follows from the mechanism, not yet tested.

### Minimum requirements (all must hold, checked in Phase 0)
| # | Requirement | How Phase 0 checks it | Evidence |
|---|---|---|---|
| R1 | The code is statically recoverable: any packer is known or crackable within the gate test (EXEPACK, LZEXE, PKLITE, DIET), and the overlay manager is identified with a parseable section table | unpack; manager named; every code byte accounted for in `LAYOUT.md` | proven: EXEPACK + Turbo Pascal FBOV (PoR); RTLink/Plus with 136 sections (Darklands); QuickBASIC 3 chained modules (Star Command) |
| R2 | The machine surface is enumerable and emulable at a high level: real-mode 8086/286, standard DOS and BIOS services, standard sound hardware, LIM EMS/XMS | list every interrupt and port the code uses; each is in the runtime or costed | proven: Darklands (DOS, BIOS, EMS, AdLib/Sound Blaster/MT-32, mouse, timer) |
| R3 | The original runs in an emulator or on real hardware, so lock-step comparison is possible | headless DOSBox-X boots the game and captures a screen | proven: all three games |
| R4 | We own the copy being decoded, and the pipeline ships nothing derived from it: translation happens on the player's machine from their own executable | the owner confirms; the release packager refuses game-derived files | proven: Darklands+ builds the game module on first start; our cases are BYO files |

### What used to be requirements and is now cost
| Factor | Stage 1 (Reproduce) | Stage 2 (Recode) |
|---|---|---|
| Naive compiler (QuickBASIC 3, Turbo Pascal 6, MS C 6 unoptimised) | irrelevant | cheap: statements map to instructions, decompiles read like source |
| Optimising compiler (Watcom, MS C with full optimisation) | irrelevant | expensive: recode fewer modules, keep the rest reproduced |
| Hand-written assembly engines | irrelevant, unless self-modifying | expensive; usually left reproduced |
| A "one layer" (runtime call table, script VM) | a service list to emulate | the cheap modules to recode first |
| No documentation, no fan format notes | irrelevant | slower cross-checks |

### Risk factors (allowed, named in the gate report)
| Risk | Why it costs | Status |
|---|---|---|
| 32-bit protected mode / DOS extenders (DOS/4GW, PMODE) | a second recompiler back end (32-bit flat, LE/LX loader) and extender services | expected; not built |
| Self-modifying code, runtime decryption, copy-protection layers | more code falls to the interpreter; decryption must be reproduced or bypassed at load | expected |
| Non-standard hardware (custom sound cards, VGA register tricks, cycle-counted timing) | runtime work per device; timing needs a cycle model the recompiler does not keep | partly seen: PC-speaker driver bytes reused directly in PoR |
| Very large code (well beyond 1 MB) | longer translation and link times; more modules to name | proven fine at 1.6 MB (Darklands) |
| Data formats needed natively (Stage 2 art, maps, saves) | each format decoded and round-tripped before a module that draws it goes native | proven: DAX, BSAVE banks, Darklands CAT/PKWARE |

### Disqualifiers (stop at Phase 0 and report to the owner; spend nothing more)
- **D1** The code cannot be made statically readable within the half-day gate test: unknown packer or encryption not cracked, or the overlay manager not identified.
- **D2** The machine surface cannot be emulated within budget: an unsupported CPU mode without a back end, or hardware the runtime cannot model (R2 fails).
- **D3** No oracle is possible: the original runs nowhere. Reproduction is still possible, but nothing can be called faithful, so it is not this method.
- **D4** Required data is missing (for example CD audio or video the copy does not include).
- **D5** The owner rules the target out (ownership, legal or priority).
- **D6** A maintained reproduction already exists under a licence we can build on. Then the case is a fork with credit, not a new pipeline (Darklands: Darklands+).

## Phases and gates
| Phase | Work | Gate to pass |
|---|---|---|
| 0. Gate test (half a day max) | **prior-art search first** (GitHub by last update, web): ports, decompilations, recompilers, format notes, with dates and licences; file inventory; executable format, packing, compiler; overlay manager identified and its table parsed; the machine surface listed (every interrupt, port, memory region); the original boots headless in DOSBox-X | pass = start Stage 1; D6 = fork; fail = report the blocker, spend nothing more |
| 1. Loader + analysis | unpacker, executable and overlay parser, whole-program recursive-descent analysis (segments, vectors, switch tables, entry points), `LAYOUT.md` | every code byte owned by a section and a function list |
| 2. Reproduce | recompiler (instruction to C over the CPU struct and flat memory; calls keep the emulated stack; indirect calls through the dispatcher; overlay vector calls bracketed; fallback interpreter for data-reached code); runtime services; the player-machine build (translation on first start) | **smoke test passes headless**: start, core loop (a battle, a turn, a level), save and load; "Play the original game" mode exists |
| 3. Playability + (optional) oracle | **autoplay** bot drives the reproduction through the whole game under node; **save swap** with original saves; the DOSBox-X lock-step oracle only at the level the owner chose at kickoff (none / minimal / medium / complete) | autoplay: every reachable area and script, 0 failures, saves round-trip; save swap passes; oracle rows at the chosen level |
| 4. Names + model | function and variable names from the one layer and the data loaders (one list shared by decompilation and port); data formats round-tripped; game-model accessors (party, inventory, map) | names ledger with H/M/L confidence; every data file mapped |
| 5. Recode modules (lanes) | per module, in the owner's order of value: decompile, pseudocode with offsets, native screen behind a hook, on/off comparison, acceptance row | each module: PASS on and off vs reference; `ACCEPTANCE.md` row |
| 6. Plus layer (standard, `docs/PLUS_LAYER.md`) | the quality-of-life package behind one master switch: hooks (events, state, click regions), panel, full clickability with right-click, automatic notes, quests, encyclopedia with reveal-on-encounter, automap, helpers, mods/skins, game profile, cheat/scenario tools, QA harness | per package: player-visible rows PASS; the whole original regression table at 0 px with Plus mounted; nothing shipped that is not the player's own or decoded |
| 7. Runtime-free product (optional) | when every module is native, drop the recompiled core: the revision-1 full rewrite (HTML5 or other engine) | every screen PASS vs reference |

## The Plus layer (standard since 2026-10-19; first built as Gold Box Plus on Pool of Radiance)
- Three layers: the engine only emits events and registers click regions; one hooks file (bus, read-only state, regions, master switch); every feature in `plus/`, writing only its own store. Input stays a key synthesizer, so "Play the original game" is provable: the full regression table at 0 px with everything mounted.
- The hook contract, the fourteen packages, their order and the traps are in `docs/PLUS_LAYER.md`. Port the contract first; the emit sites are the only per-game engine work.
- Content rule: journal booklets, manuals and art are never shipped; the player's own copy is imported like the game files and shown only once the game has referenced it.
- One implementation is a design, two are a standard: what survives Pool of Radiance and Star Command unchanged becomes the shared package; the rest stays per game.

## Acceptance (revision 2026-10-21, the owner): the remake plays itself
- **The remake, not the emulator, defines success.** "We are reproducing the game, not its emulated form." Two measurements decide: (1) **internal playability** = an autoplay bot drives the remake through the game via the engine hooks under plain node (party, every reachable area, every script, fights, camp, shop, save, reload; fails on any error, unhandled opcode, dead end, or a save that does not reload to the same state; seeded, replayable; report `acceptance/<title>/AUTOPLAY.md`); (2) **save-file swap** = data layouts proven against bytes the original wrote: import a real original save (the player's own via BYOC, or a reference save already on disk), play on, save, reload; byte compare in every defined byte where an original save of the same state exists. Behavioural correctness comes from the decode (routines translated from the original and verified against the listings), not from an oracle. Then ~6 picture-only shots (3D view, big picture, overland, font, a menu, combat board; Plus one shot per tab + the original-mode gate on those), and **the owner plays; bugs come back as fix requests.**
- **Three verification workflows, in order of cost and finality (the owner, 2026-10-23):** (1) **bot trials** = the time-boxed autoplay verdict (random policy + hinted gates) + save swap: cheap, run after every change; (2) the **DOSBox oracle**, optional, chosen at kickoff (below); (3) the **full playthrough** = the pre-release gate: a plan lane derives the game's main line from the decoded scripts (every flag, trigger, answer, exit, scripted fight, each step citing its script site; published walkthroughs consulted for order and tactics, never copied), and the bot plays it title screen to finale on the virtual clock, with the same failure criteria plus every main-line block entered. The plan is also the generated walkthrough shown to the player (spoiler-gated). **No release is called complete without a FULL PLAYTHROUGH PASS**; it is rerun after every cross-title fix and replaces the random verdict as the regression test once it exists.
- **Rigor is per engine, not per game** (the owner, 2026-10-21): the first title on an engine gets the full method; follow-up titles verify the engine delta + autoplay + save swap and ship.
- **The DOSBox oracle is optional, chosen at kickoff.** At Phase 0 the Foreman asks the owner one question (RULINGS, default = internal): *confirm completeness by internal testing, or against DOSBox?* If DOSBox: level **minimal** (one short save-byte compare: new party -> one fight -> save), **medium** (minimal + ~15 spot screens + run-throughs with saves = DOSBox), or **complete** (the full per-screen pixel table; first title on a new engine only, when the owner asks). Never a keystroke replay of a long recorded walk: it tests the emulator's keyboard and timing, not the game.

## The oracle (DOSBox-X): optional since 2026-10-21 (see Acceptance); when chosen, built in from Phase 3
- **Stage 1 is faithful by construction, but the runtime is not.** The game code is a mechanical translation; the services around it are ours. Lock-step play finds every place the runtime differs: an interrupt handler that reloaded an overlay, an EMS page mapped into the wrong frame, a timer that ticks differently. Darklands+ found all of its runtime bugs this way (garbage pictures, a party teleported by a displaced card script).
- **Stage 2 compares a module against itself.** The reference for a recoded screen is the same build with the module switched off, plus the original for the final word. A pixel match is a measurement; a model review is an opinion.
- **Any faithful way to run the original works**: DOSBox-X, 86Box, PCem, a period PC. DOSBox-X is the default because it runs headless in WSL (Xvfb, no visible window), is scriptable, and never touches the original files.
- **Rule (when the oracle level is medium or complete):** no module is called identical until its acceptance row has a reference capture that matches. At level none/minimal the decode verify + autoplay + save swap + the owner playing are the acceptance.

## Roles
- **the owner** decides: rulings (A/B), scope, model policy, the order of modules to recode.
- **the coordinator** (coordinator session): sets up repo + brief, starts the Foreman, relays rulings via sticky-ruling windows, watches milestones with Monitors, flags mistakes, reports in plain words. Never does lane work itself.
- **Foreman** (one persistent session per repo, named `<game>-foreman`): assigns lanes and models, writes assignment files, routes fix requests, enforces the gates, keeps `herdr/FOREMAN_MEMORY.md` (lessons, decisions, session ids). Restart = `claude --resume <id>`, never a second Foreman.
- **Lanes**: one task, one assignment file, one owner per output file.

## Models (policy as of 2026-10-16; the owner sets it)
- Opus: recompiler and runtime work, decode finals, tooling, verification, native modules. Proven sufficient for both stages.
- codex / Astra: heavy first drafts (pseudocode per module, data drafts, view drafts). Short prompts pointing at files.
- GLM: independent review when it has balance.
- Fable: optional bounded spot-check (~1% of the weekly budget). Never more than the owner allows; stop at 90% weekly.
- Never per-token API billing.

## File protocol (non-negotiable)
- `FOREMAN.md` brief; `STATUS.md` newest first, one block per lane result, `## HANDOFF` before any pause; `RULINGS.md` (one question, A/B, recommendation first); `REPRODUCE_GATE.md` (Phase 2 smoke and Phase 3 lock-step results); `DECODE_GATE.md` per module; `BUILD_PLAN.md`; `ACCEPTANCE.md`.
- `herdr/assignments/<lane>.md` for every lane; results only in files; commit after every result (`<lane>: <what>`).
- **Shared file = one owner.** Others write a tagged request note (`<file> request #n (topic)`); the owner answers with the same tag.
- Evidence or explicit unknown for every claim (file, offset, bytes); confidence H/M/L; no invented names.
- **One address, one name.** No raw segment:offset in native code; names come from one generated header shared by the decompilation and the port.
- Originals never modified or committed; original-derived binaries and generated game code stay out of git (the player's machine regenerates them).

## Traps already paid for (details in cases/*_FOREMAN_MEMORY.md and Darklands+ docs)
- Overlay managers: a call that loads a section can displace sections further up the call chain, not just the caller's; restore the whole displaced set on return. Interrupt handlers that load a section must save and restore the overlay area. Two sections can own the same address; dispatch by which one is resident.
- Expanded memory state must be snapshotted with the rest of memory, or "what-if" evaluations of game code corrupt the page frame.
- Coroutines on their own stacks and self-patching jump operands cannot be expressed as C; list them for the interpreter.
- Codex prompts must be 1-2 sentences pointing at files; long pastes get mangled.
- `rm -f "$VAR/..."` outside the repo blocks a bypass-mode lane on a confirm dialog; write `"${VAR:?}/..."`.
- No polling loops inside lanes (low-memory kills); the Foreman waits with `herdr agent wait` <= 300 s.
- One Ghidra at a time.
- Size the lane count with SCALING.md (about 1.5 GB RAM per working lane, one build lane per core).
- Shell-expanded prompt text (`$` in BASIC names) gets cut; single-quote prompts.
- Pascal decompiles reverse parameter order; re-check every call against the callee's declaration.
- Prose sketches of menu loops skimp on the extended-key / plain-key split.
- Herdr agent names are global across workspaces (`foreman`, `dl-foreman`, `por-foreman`).
- New repo folders show a folder-trust dialog on the first Claude start in a pane.
- Watchers that grep STATUS.md match the coordinator's own notes; grep headings (`^## `) only.
- Windows Desktop is `<Desktop>\`.
- Unsigned native builds are blocked by Smart App Control on consumer Windows 11; test in WSL, and sign or document for players.

## Product form (default)
**Stage 1 and 2:** a native program (C, SDL2) that finds the player's own copy, translates it on first start, and runs it with every modern feature switchable and "Play the original game" turning them all off; keyboard, mouse and controller; quick saves; mod folders. Windows and Linux builds; headless mode for tests. Copy protection bypassed by default behind a flag.
**Phase 7 only:** HTML5 canvas + vanilla JavaScript at original resolution, zero install, as in revision 1.
