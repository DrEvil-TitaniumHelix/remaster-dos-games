# Remaster DOS Games

**Why.** Old DOS games are locked inside their binaries: they run only under an emulator, and hardly anything about them can be changed. Recoded with this method, a game runs in a modern browser, from the copy you already own. It becomes **modifiable**: rules, screens and quality-of-life additions today, and the same route leads to new scenarios, new graphics or a different difficulty, all as edits to readable JavaScript. And it becomes **debuggable**: every routine carries its original address, so odd behaviour can be traced back to the original program and either kept, because the original did it too, or fixed.

An open method, with tools and templates, for taking an old DOS game from "nothing" to a decoded, verified, playable
rebuild in the browser, run by a team of AI coding agents. Three things you can do with it:

1. [Recode any DOS game](#1-recode-any-dos-game) — the method, gate test, tools and templates.
2. [Mod a DOS game](#2-mod-a-dos-game) — once recoded, its logic is readable JavaScript.
3. [Play the two examples](#3-play-the-two-examples) — Star Command and Pool of Radiance (SSI, 1988), alpha.

Then: [the open Darklands challenge](#open-problem-the-darklands-challenge) and
[credits, licence, disclaimer](#credits-licence-disclaimer).

## 1. Recode any DOS game

Not every DOS game is suitable, and the half-day **gate test** (`METHOD.md` §Phase 0) tells you whether yours is before
you spend more. The method works because many 1980s compilers were naive: their machine code maps almost one to one
back to source, which turns reverse engineering into translation. Proven so far on a QuickBASIC 3 game and a Turbo
Pascal 6 game, with a Microsoft C 6 game decoded in part (`COMPATIBILITY.md`).

The method in one paragraph: check the target against the suitability rules; read the whole program statically, not
by watching it run; find and crack the one layer every piece of logic passes through (a language runtime, an overlay
manager, a script VM) and name it once; split the rest into areas, each decoded to pseudocode by its own agent lane
under one persistent Foreman; keep every fact in committed files; verify every area with an independent lane and a
DOSBox-X pixel oracle; build only once the decode gate is met, by translating the verified pseudocode into a browser
engine and comparing every screen with the original.

**How it runs** (`ARCHITECTURE.md`): the rebuilt games are plain JavaScript on an HTML5 canvas, no framework and no
build step; the decode side is Python and Ghidra. The work is done by an adaptable agent graph in
[Herdr](https://herdr.dev): one persistent Foreman per game starts, reuses and closes lanes phase by phase from the
repo's own files, and three flat-rate model subscriptions have fixed, replaceable roles.

Read in this order:
1. `METHOD.md` — the rulebook: principles, suitability rules, phases, gates, roles, file protocol, traps.
2. `ARCHITECTURE.md` — what gets built and how the agents run: the Herdr agent graph, model roles, memory limits,
   lane suggestions per machine and phase.
3. `SCALING.md` — how many lanes: about 1.5 GB of RAM per working lane plus fixed reserves; about 6 on a 16 GB
   handheld, 12-16 on a 128 GB desktop; and why more does not help.
4. `COMPATIBILITY.md` + `profiles/` — which original compilers and runtimes are proven, and how to add one.
5. `templates/` — copy into a new game repo: Foreman briefs, decode gate, build plan, lane assignments (each with a
   worked example from the two cases).
6. `tools/` — starters: DOS MZ parser, 16-bit disassembler, EXEPACK unpacker, Turbo Pascal overlay splitter, context
   grepper, and the personal-data gate used before publishing.
7. `CASES.md` + `cases/` — the games behind the method, lessons learned, and the independent spot-check of a decode.
8. `RELEASE.md` — the repeatable process that turns a private decode workspace into a public game repo.

Starting a new game:
1. Put your original files in a folder outside every repo (never modified, never committed).
2. Run the gate test (`METHOD.md` §Phase 0). Stop and report if it fails; a failure is a useful
   `COMPATIBILITY.md` result too.
3. Create the game repo; copy `templates/FOREMAN_example_*.md` to `FOREMAN.md` and edit the target facts; copy
   `templates/assignments/` and `tools/`.
4. Open a Herdr workspace, start the Foreman (`<game>-foreman`) with: read `FOREMAN.md` and `cases/LESSONS.md`, start
   phase 1.
5. You decide the rulings the Foreman asks for; everything else is in the files.

## 2. Mod a DOS game

A recoded game is readable JavaScript organised like the original program, every routine tagged with its original
address, with the decoded pseudocode and data specs in the same repo. Changing a rule or a screen is an edit, not a
reverse-engineering project. How each example is laid out, and where to make a change, is in its README under
*Modify*: engine, game logic, acceptance screens, unit tests. Neither game repo contains the original's files; you
play and test with your own copy.

## 3. Play the two examples

Both run in a browser from a small local web server and need your own copy of the game (checked by file hash, kept in
browser storage, never uploaded). Alpha: ready for community testing; please report problems in each repo's Issues.

| Game | Original | Status (v0.1.0-alpha) | Repo |
|---|---|---|---|
| Star Command (SSI, 1988) | QuickBASIC 3 + BRUN30 | 90 acceptance screens, 90 pass; 64 compared with the original in DOSBox: 62 match apart from test data, none differ, 2 cannot be shown | https://github.com/DrEvil-TitaniumHelix/star-command-remake |
| Pool of Radiance (SSI, 1988) | Turbo Pascal 6 + overlays, EXEPACK | 105 screens tracked: 69 pixel-exact, 25 differ for documented reasons, 8 not reached yet; all 29 script areas play in an automated sweep; overland map and endgame not verified yet | https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake |

## Open problem: the Darklands challenge

Darklands (MicroProse, 1992; Microsoft C 6 with compressed overlays) is decoded in part and has no rebuild. Everything
known so far, and where earlier attempts stalled, is in [cases/DARKLANDS_CHALLENGE.md](cases/DARKLANDS_CHALLENGE.md).
Nobody has finished it.

## Pull requests

Decode work most of all: a new compiler profile (success or failure), a link to your own game case, a better tool, a
fix to the method. `CONTRIBUTING.md` says what a pull request must never contain (original files or anything
extracted from them) and what it must have (evidence for every claim).

## Credits, licence, disclaimer

- Method, tools and templates: **DrEvil** (DrEvil and Titanium Helix LLC).
- Code: MIT (`LICENSE-MIT`); documentation: CC BY 4.0 (`LICENSE-DOCS`); see `LICENSE`.
- The games named here belong to their authors and publishers; this repository contains no game material.

Disclaimer: all or part of this repository may have been written or edited by super intelligence
