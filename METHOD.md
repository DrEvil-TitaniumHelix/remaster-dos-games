# METHOD — the rulebook

## Why it works (the causes, in order of weight)
1. **Static, whole-program, disassembly-first.** Every byte of code is extracted and owned by a lane. Coverage is 100% by construction. Dynamic routes (record what runs while playing) stall: Darklands' earlier attempt reached ~21% code coverage; earlier Gold Box attempts worked from behaviour and reached ~15% of a game.
2. **Crack the one layer first.** Every game has a choke point all logic passes through. Star Command: 140 BRUN30 runtime routines called through INT 3Dh-3Fh tables. Pool of Radiance: the Turbo Pascal overlay layout, then the 61-opcode ECL script VM. Decode it once; the rest becomes mechanical, parallel work.
3. **Many fresh contexts, one persistent Foreman (Herdr).** A single session cannot hold a whole game (Pool of Radiance listings ~149,000 lines); it compacts, loses exact facts, then guesses. Lanes each hold one area; the Foreman holds the big picture and long memory.
4. **State lives in files, never in chat.** Assignments, STATUS notes, pseudocode, rulings, memory: all committed. Any lane or Foreman can crash, hit a usage limit or be replaced and resume from the files.
5. **Independent verification before trust.** A different lane (and ideally a different model) re-reads a sample of every area against the bytes; the build catches errors; a headless DOSBox-X oracle compares pixels. Errors are caught in hours, not weeks.
6. **Decode gate before build.** No engine work until the checklist is ticked with evidence (the owner may order build to start in parallel with the last verification items; then translate an area only after its verification passes).
7. **Build = translation.** Verified pseudocode is translated into the engine (generated where possible, e.g. Star Command's bas2js), plus a thin engine (display, text, input, audio, file I/O, module chaining). Not a redesign.

The model is NOT the key ingredient: Pool of Radiance was decoded entirely on Opus + codex/Astra with zero refusals; a Fable spot-check rated it 27/30 routines exact (90%), with no wrong formula, offset or constant. REA is a first-hour survey tool only (it cannot see overlays or follow compiled-BASIC runtime calls).

## The core mechanism: reverse engineering turned into translation
Best current explanation (a hypothesis supported by two games, not a controlled experiment):
1. 1980s high-level compilers were naive. QuickBASIC 3 and Turbo Pascal 6 did almost no optimisation, so each source statement compiles to a predictable instruction pattern and the machine code maps nearly one to one back to source.
2. Tools first, AI second. The first hours build tools that unpack, split overlays and label every runtime call; after that a listing reads like source with the names stripped.
3. Turning near-source into clean pseudocode is a translation task, which language models do extremely well; inferring hidden logic from raw bytes or from watching the game run is not. This is why Opus was enough.
4. Completeness is countable (every function owned, a gate checklist) and correctness is measurable (pixel comparison against the original).
Herdr lanes are the multiplier (speed, small exact contexts), not the root cause. The suitability rules below follow from this mechanism: the closer the machine code is to its source, the better the method works.

## Target suitability: minimum requirements, risk factors, disqualifiers
Status legend: **proven** = done on a real game; **expected** = follows from the mechanism, not yet tested.

### Minimum requirements (all must hold, checked in Phase 0)
| # | Requirement | How Phase 0 checks it | Evidence |
|---|---|---|---|
| R1 | The code is statically recoverable: any packer is a known one or crackable within the gate test (EXEPACK, LZEXE, PKLITE, DIET), and overlays have a parseable layout | unpack, then every code byte accounted for in `LAYOUT.md` | proven: EXEPACK + Turbo Pascal FBOV overlays (PoR); PKWARE-imploded overlays with a resident directory (Darklands) |
| R2 | The logic is high-level-compiled with a non-optimising compiler, or runs on a bytecode/script VM | compiler ID from runtime strings and code idioms; Ghidra decompiles real engine functions coherently | proven: QuickBASIC 3 (Star Command), Turbo Pascal 6 (PoR); MS C 6 decompiled well in Darklands overlays |
| R3 | A "one layer" exists and can be located: a language runtime with a call table, an overlay manager, or a script VM with an opcode dispatch table | dispatch table found and a sample of entries named | proven: BRUN30 140 routines; ECL VM 61 opcodes |
| R4 | The data files are present and their formats are recoverable from the code that loads them | one format round-trips (decode, render, compare) | proven: DAX containers, BSAVE sprite banks |
| R5 | The original runs in an emulator or on real hardware, so an oracle exists | headless DOSBox-X boots the game and captures a screen | proven: both games |
| R6 | We own the copy being decoded | the owner confirms | the owner's call |

### Risk factors (allowed, but each one raises effort and must be named in the gate report)
| Risk | Why it hurts the mechanism | Status |
|---|---|---|
| Optimising compilers (Watcom C/C++, Microsoft C with full optimisation, later Borland with optimisations on) | inlining, register allocation and code motion break the statement-to-instruction mapping; translation becomes inference again | expected |
| Hand-written assembly engines (common in action games, 3D engines, demoscene-style code) | no source statements to recover; logic is spread through registers and tricks | expected |
| 32-bit protected mode / DOS extenders (DOS/4GW, PMODE) | larger code, usually Watcom-optimised, different executable formats (LE/LX) needing new tooling | expected |
| Self-modifying code, runtime decryption, custom packers or copy-protection layers | static listings no longer show what runs | expected |
| Timing- or hardware-dependent behaviour (cycle-counted loops, VGA register tricks, custom sound drivers) | the logic can be decoded, but a faithful reproduction needs hardware-level emulation of those parts | partly seen: PC-speaker driver bytes reused directly in PoR |
| Very large code (well beyond ~300 KB of game code) | more areas and lanes, longer critical path, more cross-area globals | expected |
| No documentation and no fan format notes | none of our wins relied on them, but they speed up cross-checks | proven not required |

### Disqualifiers (stop at Phase 0 and report to the owner; spend nothing more)
- **D1** The code cannot be made statically readable within the half-day gate test: unknown packer or encryption not cracked, or overlays not locatable.
- **D2** Ghidra cannot produce coherent decompiles of real engine functions, and no runtime or VM layer is found (R2 and R3 both fail). The method would fall back to raw-assembly inference, which is the failure mode of the earlier attempts.
- **D3** No oracle is possible: the original does not run in any emulator or on available hardware. Building is still possible, but nothing can be called faithful, so it is not this method.
- **D4** Required data is missing (for example CD audio or video the copy does not include).
- **D5** the owner rules the target out (ownership, legal or priority).
Two or more expected risk factors together (for example a Watcom-compiled, protected-mode, assembly-heavy action game) should be treated as a probable disqualifier until a gate test proves otherwise.

## Phases and gates
| Phase | Work | Gate to pass |
|---|---|---|
| 0. Gate test (half a day max) | file inventory; executable format, compiler/runtime ID, packing (EXEPACK, LZEXE, PKLITE), overlays; Ghidra decompiles real engine functions; the one layer located with its dispatch table; one data format round-trips | pass = start lanes; fail = report the blocker to the owner, spend nothing more |
| 1. Toolchain | unpacker, loader/overlay parser, runtime-aware disassembler, Ghidra headless project with every code unit at its own segment, listings export | full listings of every code unit; `LAYOUT.md` |
| 2. One layer + data (parallel) | runtime/VM naming ledger with H/M/L confidence; data lane: containers, compression, pictures (PNG renders), maps, records, saves | ledger verified; every data file mapped to spec + loader |
| 3. Area lanes | per module/overlay group: codex drafts, Opus/Fable finals: pseudocode with offsets as labels, `<AREA>_SCREENS.md`, names json, self-check, argument-order audit | all areas FINAL |
| 4. Verification + CROSSREF | independent re-read of sampled statements per area; shared globals and call graph; screen index | `DECODE_GATE.md` all ticked; the coordinator declares the gate to the owner |
| 5. Build | `BUILD_PLAN.md`; engine lane; area translation lanes; `ACCEPTANCE.md` one row per screen; integration runs end to end | every screen PASS vs reference; a playable launcher + Desktop shortcut |
| 6. Oracle | headless DOSBox-X in WSL (Xvfb, no visible window) captures reference screens; pixel comparison; decode-error classes routed back | reference rows PASS |
| 7. Polish (on the owner's request) | mouse, Esc save/quit, control overlay, zoom, tooltips, QoL features, each toggled, plus Classic mode; prebuilt test save + shortcut | per feature: tests, review, acceptance unchanged in Classic mode |

## The oracle (DOSBox-X): optional for "playable", required for "faithful"
- **Not needed to reach playable.** Star Command passed its decode gate and reached playable v1 (83/83 screens passing AI review against the decode) before any DOSBox lane existed.
- **Required to prove faithful.** When the original was then run headless as a reference, pixel comparisons found three decode-error classes that every review had passed: a misread graphics drawing mode (PUT verbs), an absolute-value idiom misread as negation (ABS), and folded array indexes. Each touched several screens. Without the oracle the remake would have looked plausible and been subtly wrong.
- **It is the only objective evidence.** Pool of Radiance's title, first script text and explore screen each match the original at 0 differing pixels. Model reviews (including the Fable spot-check) are informed opinions; a pixel match is a measurement.
- **Any faithful way to run the original works**: DOSBox-X, 86Box, PCem, or a real period PC. DOSBox-X is the default because it runs headless in WSL (Xvfb, no visible window), is scriptable (keys, timing, capture), and never touches the original files.
- **Rule:** the decode and build may run without it, but no screen is called identical, and no release is called faithful, until its acceptance row has a reference capture that matches. Start the oracle lane as soon as the build shows its first screen, and route every mismatch back to the decode, not just to the engine.

## Roles
- **the owner** decides: rulings (A/B), scope, model policy, when to build.
- **the coordinator** (coordinator session): sets up repo + brief, starts the Foreman, relays rulings via sticky-ruling windows, watches milestones with Monitors, flags mistakes, reports in plain words. Never does lane work itself.
- **Foreman** (one persistent session per repo, named `<game>-foreman`): assigns lanes and models, writes assignment files, routes fix requests, enforces the gate, keeps `herdr/FOREMAN_MEMORY.md` (lessons, decisions, session ids). Restart = `claude --resume <id>`, never a second Foreman.
- **Lanes**: one task, one assignment file, one owner per output file.

## Models (policy as of 2026-10-16; the owner sets it)
- Opus: decode finals, tooling, verification, build. Proven sufficient for decode.
- codex / Astra: heavy first drafts (pseudocode per area, data drafts, build drafts). Short prompts pointing at files.
- GLM: independent review when it has balance.
- Fable: optional bounded spot-check (~1% of the weekly budget for 30 routines + 8 opcodes + 3 formulas). Never more than the owner allows; stop at 90% weekly.
- Never per-token API billing.

## File protocol (non-negotiable)
- `FOREMAN.md` brief; `STATUS.md` newest first, one block per lane result, `## HANDOFF` before any pause; `RULINGS.md` (one question, A/B, recommendation first); `DECODE_GATE.md`; `BUILD_PLAN.md`; `ACCEPTANCE.md`.
- `herdr/assignments/<lane>.md` for every lane; results only in files; commit after every result (`<lane>: <what>`).
- **Shared file = one owner.** Others write a tagged request note (`<file> request #n (topic)`); the owner answers with the same tag.
- Evidence or explicit unknown for every claim (file, offset, bytes); confidence H/M/L; no invented names.
- Originals never modified or committed; original-derived binaries stay out of git (regenerate them with the tools).

## Traps already paid for (details in cases/*_FOREMAN_MEMORY.md)
- Codex prompts must be 1-2 sentences pointing at files; long pastes get mangled.
- `rm -f "$VAR/..."` outside the repo blocks a bypass-mode lane on a confirm dialog; write `"${VAR:?}/..."`.
- No polling loops inside lanes (low-memory kills); the Foreman waits with `herdr agent wait` <= 300 s.
- One Ghidra at a time.
- Size the lane count with SCALING.md (about 1.5 GB RAM per working lane, one build lane per core); overloading the machine slows every lane and gets processes killed.
- Shell-expanded prompt text (`$` in BASIC names) gets cut; single-quote prompts.
- Pascal decompiles reverse parameter order; re-check every call against the callee's declaration (the one error class Fable found).
- Prose sketches of menu loops skimp on the extended-key / plain-key split.
- Herdr agent names are global across workspaces (`foreman`, `dl-foreman`, `por-foreman`).
- New repo folders show a folder-trust dialog on the first Claude start in a pane.
- Watchers that grep STATUS.md match the coordinator's own notes; grep headings (`^## `) only.
- Windows Desktop is 's: `<Desktop>\`.

## Product form (default)
HTML5 canvas + vanilla JavaScript, original resolution scaled up, keyboard + Gamepad API + mouse, zero install, runs in Chrome app mode from a `.cmd` launcher and a Desktop shortcut, local server with caching off, screenshot-verifiable headless. Sprites from a PNG atlas so art can be swapped later. Copy protection bypassed by default behind a flag.
