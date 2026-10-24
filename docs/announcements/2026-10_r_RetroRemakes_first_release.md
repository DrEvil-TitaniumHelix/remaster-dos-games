# r/RetroRemakes — first release post (DRAFT v5, 2026-10-18: three things = recode / mod / play; wording per CLAIMS.md audit A1-A16; the owner posts)

**Title (owner, 19:00):** An open toolkit and architecture to remaster DOS games

(Previous title kept as the optional tail if Reddit needs more context: "recode any DOS game, mod it, play it. First two examples: Star Command and Pool of Radiance (SSI, 1988), alpha.")

**Body:**

Open toolkit, open method, open architecture.

**Why.** Old DOS games are locked inside their binaries: they run only under an emulator, and hardly anything about them can be changed. Recoded with this method, a game runs in a modern browser, from the copy you already own. It becomes **modifiable**: rules, screens and quality-of-life additions today, and the same route leads to new scenarios, new graphics or a different difficulty, all as edits to readable JavaScript. And it becomes **debuggable**: every routine carries its original address, so odd behaviour can be traced back to the original program and either kept, because the original did it too, or fixed.

Three things you can do with this, in one open toolkit:

**1. Recode any DOS game.** A documented method takes an old DOS game from "nothing" to a decoded, verified, playable rebuild. It works because many 1980s compilers were naive: their machine code maps almost one to one back to source. Account for every byte of code, name the language runtime once, read each module as the program it was. A half-day gate test tells you whether your game is suitable before you spend much. Then: static whole-program disassembly, per-module pseudocode, independent verification, a DOSBox pixel oracle, translation into a browser engine.

*How it runs.* The rebuilt games are plain JavaScript on an HTML5 canvas: no framework, no build step, any static web server; the decode side is Python and Ghidra. The work is done by an adaptable agent graph in Herdr: one persistent Foreman session per game plans the work and starts, reuses and closes worker lanes phase by phase (survey, runtime naming, per-module decode, independent verification, build, DOSBox oracle), reshaping the graph from the repo's own files. Agents talk only through committed files, one owner per file, so any lane can be replaced mid-run. Three flat-rate subscriptions have fixed roles: Claude Opus for the Foreman, finals, verification and build, OpenAI Codex for bulk first drafts, Z.ai GLM for independent review; any of them can be dropped and its role moved. A 16 GB handheld runs about 6 lanes, a 128 GB desktop 12-16 (ARCHITECTURE.md).

Method, tools, templates and two worked cases: https://github.com/DrEvil-TitaniumHelix/remaster-dos-games

**2. Mod a DOS game.** Once a game is recoded, its logic is readable JavaScript organised like the original program, every routine tagged with its original address, with the decoded pseudocode and data specs in the same repo. Changing a rule or a screen is an edit, not a reverse-engineering project.

**3. Play the two examples**, in a browser, alpha:
- **Star Command** (SSI, 1988, QuickBASIC): 90 acceptance screens, 90 pass. 64 of them were compared with the original running in DOSBox: 62 match apart from test data such as crew names and dice rolls, none differ, 2 cannot be shown in the original. Mouse, gamepad, zoom, save slots, and a Classic mode that switches every convenience off. https://github.com/DrEvil-TitaniumHelix/star-command-remake
- **Pool of Radiance** (SSI, 1988, Turbo Pascal with overlays): 105 screens tracked: 69 match the original pixel for pixel, 25 differ for documented reasons, 8 are not reached yet (overland map, endgame, a few rare events). Every town and dungeon area loads and plays in an automated sweep, 29 of 29; the overland map and the endgame are not verified yet. The rougher alpha of the two. https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake

Bring your own copy: neither repo contains the games' files, no program, data, graphics or sound (the decode notes quote game text where it serves as evidence). On first start the browser asks for your own game folder, checks it by file hash (Pool of Radiance needs version 1.3), keeps it in local browser storage, and never uploads anything. Star Command translates its program modules in your browser from your own copy; Pool of Radiance ships them. The engines come from an analysis of the original programs, not clean-room; all rights to the games stay with their authors and publisher.

**Try Darklands.** Everything known so far is posted as an open challenge: the overlay directory, 81 overlays, a proven route to a full Ghidra export, Microsoft C 6 code that decompiles well, and the two places where earlier attempts stalled. Nobody has finished it. Have a go.

**Pull requests, please.** Decode work most of all: a new compiler profile, a link to your own game case, a better tool, a fix to the method. The method repo's contributing guide says what a PR must never contain (original files or anything extracted from them) and what it must have (evidence for every claim). Bug reports go to each repo's Issues: name the screen, attach a save if you have one, say which browser.

Disclaimer: all or part of this post may have been written or edited by super intelligence

---
Claim log: see CLAIMS.md (release lane audit, 2026-10-18). v5 applies its SOFTEN wordings A4, A6, A7, A9, A15, A16 verbatim or near-verbatim; A12 (GOG) stays dropped. Darklands paragraph pending the challenge page (must name the two stall points: dynamic coverage route ~21%, 16-bit overlay wall).

---
## Posting plan (owner 17:55): 1. r/dosgaming (tools-led variant below), 2. r/ClaudeCode / r/ClaudeAI (Built-with-Claude flair + a comment on how Claude was used = the architecture paragraph) or r/retrogaming (games-led variant below), 3. THEN crosspost both to the owner's r/RetroRemakes (Reddit crosspost of the r/dosgaming one; the main three-things text can be its pinned follow-up). Reddit is not readable from this machine: the owner checks each sidebar before posting.

### r/retrogaming (games-led; attach 3-4 screenshots; one link in the body, the rest in a first comment)
**Title:** Star Command and Pool of Radiance (SSI, 1988) rebuilt as browser games from a full decode of the originals, open source, bring your own copy

**Body:**
Two SSI classics running in a browser, rebuilt from a complete decode of the original DOS executables rather than re-imagined. Star Command: 90 acceptance screens, 90 pass, 64 compared against the original in DOSBox. Pool of Radiance: 105 screens tracked, 69 match the original pixel for pixel; the overland map and endgame are not verified yet, so call it alpha.

Neither repo contains the games' files. On first start the browser asks for your own copy, checks it by hash, and keeps it in local storage. Mouse and gamepad added; a Classic mode switches every addition off. All rights to the games stay with their authors and publisher.

Repos, the method they were built with, and an open Darklands challenge in the first comment. Bug reports welcome: name the screen, attach a save, say which browser.

Disclaimer: all or part of this post may have been written or edited by super intelligence

*First comment:* the three repo links + "Everything was built with an open method and toolkit; if you want to recode a DOS game yourself, start with the half-day gate test in the method repo."

### r/dosgaming (owner 17:25: tools prominent; the games are the proof)
**Title:** An open toolkit and architecture to remaster DOS games: method, tools and templates to decode a DOS executable and rebuild it in the browser. Two finished examples (SSI 1988), one open challenge (Darklands)

**Body:**
Not a replacement for DOSBox or real hardware: this is about reading the programs themselves. **Remaster DOS Games** (https://github.com/DrEvil-TitaniumHelix/remaster-dos-games) is a documented method with tools and templates for taking a DOS game from the raw executable to a full decode (every byte of code accounted for, the compiler runtime named, each module as pseudocode) and then to a verified rebuild that is checked screen by screen against the original running in DOSBox. The original stays the reference throughout, and you need your own copy of it:

- **Gate test (half a day):** file inventory, executable format, compiler or runtime ID, packing and overlays; Ghidra must decompile real engine functions; one data format must round-trip. Pass means the game is suitable; fail means stop before spending anything.
- **Tools in the repo:** DOS MZ parser, 16-bit disassembler, EXEPACK unpacker, Turbo Pascal overlay splitter, context grepper; compiler profiles for QuickBASIC 3, Turbo Pascal 6 and Microsoft C 6 that say what each runtime looks like in the binary and how to name it once.
- **Pipeline:** static whole-program disassembly, per-module pseudocode with every routine tagged by its original address, independent verification by a second model, a DOSBox pixel oracle, then translation into an HTML5 engine. Templates for the Foreman brief, decode gate, build plan and lane assignments are included.
- **Scaling notes:** about 1.5 GB of RAM per working lane; what fits on a 16 GB machine and on a 128 GB one.

**Proof it works**, both playable in a browser, alpha, bring your own copy (the repos hold none of the games' files; the browser checks your copy by hash and keeps it in local storage):
- Star Command (QuickBASIC): 90 acceptance screens, 90 pass, 64 compared against the original in DOSBox. https://github.com/DrEvil-TitaniumHelix/star-command-remake
- Pool of Radiance (Turbo Pascal with overlays): 105 screens tracked, 69 pixel-identical to the original; overland and endgame not verified yet. https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake

Once a game is recoded its logic is readable JavaScript next to the decoded pseudocode, so a rule change or a new screen is an edit, not a reverse-engineering project.

**Open challenge: Darklands.** Everything known is posted: the overlay directory, 81 overlays, a proven route to a full Ghidra export, Microsoft C 6 code that decompiles well, and where two earlier attempts stalled. Pull requests to the method, the profiles and the tools are the point of publishing this.

Disclaimer: all or part of this post may have been written or edited by super intelligence

### Compliance checklist (apply to every sub; owner verifies against the sidebar since Reddit is unreachable from the handheld)
1. Self-promotion ratio: post from the account that comments elsewhere in the sub; one post per sub, no reposts.
2. No links to game downloads of any kind; BYOC sentence present; no mention of where any copy came from.
3. AI-content rules: several retro subs remove AI-generated images or text. The disclaimer line is kept by the owner's rule; if a sub bans AI-written text outright, the owner decides whether to post there at all.
4. Flair: pick "Project", "Homebrew", "Discussion" or the nearest; never "News".
5. Screenshots show the remake, not scans of the manual or box art.
6. Reply to every comment within the first hours; the "original did this too" label exists for a reason.

### r/ReverseEngineering (owner 19:40: "we really are doing reverse engineering"; technical, no marketing; link-style post with the method repo as the link, this text as the body or first comment)
**Title:** Static whole-program decode of two 1988 DOS games (QuickBASIC 3 runtime; Turbo Pascal 6 overlays + a script VM) to verified browser rebuilds, with the method, tools and a pixel oracle published

**Body:**
Write-up and repos for a method that takes a 16-bit DOS executable to a complete decode and then to a rebuild that is compared screen by screen against the original. Two finished cases, one in progress, one open.

**Approach.** Static and whole-program: every code byte is extracted and owned (resident image, unpacked EXEPACK, every overlay at its own load segment) before any naming starts. Then the "one layer" every piece of logic passes through is cracked once: the language runtime, the overlay manager, or a script VM. After that each module reads as the program it was and is written out as pseudocode with every routine tagged by its original address. An independent lane re-reads sampled statements, and a headless DOSBox-X capture of the original is the oracle: 0 differing pixels is the pass condition for a screen. The build is a translation of the verified pseudocode into plain JavaScript on canvas.

**Case 1, Star Command (SSI 1988, QuickBASIC 3).** The runtime BRUN30 exposes 140 routines through interrupt-vectored dispatch tables; naming all 140 turned every module listing into near-BASIC. 90 acceptance screens pass; 64 have DOSBox references, 62 match apart from test data. Three decode-error classes were found only by the oracle, not by review: a misread graphics PUT mode, an abs() idiom read as negation, folded array indexes.

**Case 2, Pool of Radiance (SSI 1988, Turbo Pascal 6).** EXEPACK-packed START.EXE, FBOV overlay file, and an event-script VM (61 opcodes) that drives the game: the VM is the one layer, the overlays are loaded into Ghidra at their own segments. 105 screens tracked, 69 pixel-identical, 25 differences with stated causes, the rest not reached yet.

**In progress: Starflight 2 (1989)**, a FORTHOUGHT 2.52 indirect-threaded Forth image with 65 overlays inside two block databases and 194 machine-code primitives; the gate test passed in twenty minutes of lane time. **Open: Darklands (MS C 6, 81 PKWARE-imploded overlays)**, posted as a challenge with the two places earlier attempts stalled.

**Tooling.** Python (MZ parser, 16-bit disassembler, EXEPACK unpacker, TP overlay splitter), Ghidra headless, DOSBox-X under Xvfb. The work is run by a graph of AI coding agents under one persistent foreman per game, talking only through committed files; details in ARCHITECTURE.md. Nothing original ships: the rebuilds import the player's own copy, checked by hash.

Method, tools, compiler profiles: https://github.com/DrEvil-TitaniumHelix/remaster-dos-games
Cases: https://github.com/DrEvil-TitaniumHelix/star-command-remake , https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake

Disclaimer: all or part of this post may have been written or edited by super intelligence
