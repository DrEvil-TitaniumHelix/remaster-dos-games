# CLAIMS — audit of the first-release announcement (drafts v2 and v4) and the two public game READMEs

Lane `release`, 2026-10-18. Every factual claim in `2026-10_r_RetroRemakes_first_release.md` (v2) and in the READMEs of the
two public candidates, checked against the **public trees** (`star-command-remake` = StarCommand-public,
`pool-of-radiance-remake` = PoolRadianceRE-public), not the private workspaces. Verdicts: **KEEP** (evidence in the public
tree), **SOFTEN** (true only in a narrower form: use the replacement wording), **DROP** (no evidence, or false).
SC = Star Command, PoR = Pool of Radiance. File:line refers to the public trees at SC 34203a6 / PoR 8fcd2c9.

**Current draft = v4** (three things: recode / mod / play, then Darklands + pull requests). Section A0 audits every v4
sentence; sections A-C hold the evidence rows A0 refers to (written against v2, still valid). Section E is v4 with all
replacements applied.

## A00. Draft v5 deltas (2026-10-18; rows A0 still apply where v5 kept v4 wording)

| # | v5 sentence | verdict / replacement |
|---|---|---|
| W1 | Title "An open engine to remaster DOS games" (also the r/dosgaming title) | **SOFTEN**: there is no shared engine; the method repo holds a method, tools and templates, and each game has its own engine (`ARCHITECTURE.md` §1). → "An open toolkit to remaster DOS games". |
| W2 | Heading 1 "Recode any DOS game" | **KEEP by owner ruling (16:55)** against V1's evidence; the body must carry the caveat: keep "A half-day gate test tells you whether your game is suitable" and add "proven so far on QuickBASIC and Turbo Pascal games" (`COMPATIBILITY.md`). |
| W3 | Heading 1 still says "1980s compilers produced …", "list every byte", "before you spend anything" | apply V4, V5, V6. |
| W4 | "How it runs" paragraph (added by this lane) | sourced from `ARCHITECTURE.md` (METHOD.md principles 3-4, roles; SCALING.md numbers). **KEEP**. |
| W5 | Darklands paragraph unchanged from v4 ("a working Ghidra export", "decompiles cleanly") | apply V22, V23; the challenge page (`cases/DARKLANDS_CHALLENGE.md`) names both stall points, so V24 holds. |
| W6 | PR paragraph unchanged from v4 | apply V26, V27. |
| W7 | r/retrogaming variant: "rebuilt from a complete decode", 90/90, 64 compared, 105/69, BYOC, "Mouse and gamepad added", Classic mode | **KEEP** (A1, A3, A4, A5, A6, A10). |
| W8 | r/dosgaming: "Two finished examples" | **SOFTEN** → "two playable alpha examples". |
| W9 | r/dosgaming: "fail means stop before spending anything" | **SOFTEN** → "fail means stop after half a day". |
| W10 | r/dosgaming: "independent verification by a second model" | **SOFTEN**: Star Command used a second model (GLM) on 4 of 7 modules plus independent Opus lanes; Pool of Radiance used independent Opus lanes and a Fable spot-check. → "independent verification by a separate lane, a second model where available". |
| W11 | r/dosgaming: tools list, profiles for QB3 / TP6 / MS C 6, templates, scaling numbers | **KEEP** (`tools/`, `profiles/`, `templates/`, `SCALING.md`). |

## A000. "Why" block (owner, 18:20; README top + first paragraph of the post)

| # | owner's wording | evidence | verdict / wording used |
|---|---|---|---|
| Y1 | "they run only under an emulator, and nothing about them can be changed" | rhetorical; binary patching and mods exist for some games | **SOFTEN** → "hardly anything about them can be changed" |
| Y2 | "a game runs anywhere a browser runs, from the copy you already own" | both games need a local web server and are tested in Chrome (Edge recommended); phones and other browsers untested; BYOC import (A10) | **SOFTEN** → "a game runs in a modern browser, from the copy you already own" |
| Y3 | "modifiable: new scenarios, new graphics, quality-of-life additions, difficulty, whatever you want, as edits to readable JavaScript" | rules, screens and QoL: yes (SC v1.1-v1.3 additions; A15/A16). Sprites and scenarios have no override path yet (V10). Difficulty = rule edits (yes). | **SOFTEN** → "rules, screens and quality-of-life additions today, and the same route leads to new scenarios, new graphics or a different difficulty, all as edits to readable JavaScript" |
| Y4 | "debuggable: every routine carries its original address" | A15: PoR `{ seg:off }` per routine in `game/areas/*.js`; SC generated modules keep the original offsets as labels, hand-written code cites them | **KEEP** |
| Y5 | "traced back … and either kept, because the original did it too, or fixed" | PoR `docs/DEVIATIONS.md` (#r2-2 confirmed as original behaviour in DOSBox); SC `acceptance/DOSBOX_REQUESTS.md` (13+ questions settled) | **KEEP** |

## A0. Announcement draft v4 (authoritative)

| # | v4 sentence | evidence | verdict / replacement |
|---|---|---|---|
| V1 | Title "Remaster DOS Games: recode **any** DOS game, mod it, play it" | `COMPATIBILITY.md`: 2 toolchains proven (QB3 oracle-verified, TP6 decoded + alpha build), MS C 6 decoded partial, everything else untested; optimising compilers and hand-written assembly **expected hard**; SCUMM/SCI/AGI out of scope. `PUBLISHING_CHECKLIST.md` item 6 forbids an "almost any DOS game" claim until COMPATIBILITY.md supports it. | **SOFTEN** → "Remaster DOS Games: recode a DOS game, mod it, play it. First two examples: Star Command and Pool of Radiance (SSI, 1988), alpha. Pull requests wanted." |
| V2 | "1. Recode any DOS game." heading | as V1 | **SOFTEN** → "**1. Recode a DOS game.**" |
| V3 | "from 'nothing' to a decoded, verified, playable rebuild" | both cases (A1, A3, A6) | **KEEP** |
| V4 | "It works because 1980s compilers produced machine code that maps almost one to one back to source" | `METHOD.md` suitability rule R2: *non-optimising* compilers or a bytecode VM; proven on QB3, TP6, MS C 6 | **SOFTEN** → "It works because many 1980s compilers were naive: their machine code maps almost one to one back to source." |
| V5 | "list every byte, name the language runtime once, read each module as the program it was" | `METHOD.md:4` principle 1 (every byte of code extracted, 100% coverage by construction); the one layer (runtime / overlay manager / VM) | **SOFTEN** "list every byte" → "account for every byte of code". |
| V6 | "A half-day gate test tells you whether your game is suitable before you spend anything" | `METHOD.md` §Phase 0 | **SOFTEN** "before you spend anything" → "before you spend much" (the gate itself costs half a day). |
| V7 | pipeline list ending "translation into a browser engine" | A18 | **KEEP** |
| V8 | "Method, tools, templates and two worked cases" + link | `METHOD.md`, `tools/`, `templates/` (FOREMAN / BUILD_PLAN / DECODE_GATE examples for both games), `CASES.md`, `cases/LESSONS.md` | **KEEP** |
| V9 | "2. … its logic is readable JavaScript, one module per original program module, with the decoded pseudocode and data specs beside it" | A15: true for PoR (committed per overlay); SC generates its five big modules in the browser from the player's copy | **SOFTEN** → "Once a game is recoded, its logic is readable JavaScript organised like the original program, every routine tagged with its original address, with the decoded pseudocode and data specs beside it." |
| V10 | "A new rule, a changed screen, a redrawn sprite, a scenario tweak: an edit" | A16. Rules / screens: yes (PoR `game/areas/*.js`; SC module override in `game/modules/`). Sprites come from the player's own files at runtime; no override path exists (PoR `BUILD_PLAN.md:28` "a later art pass … deferred"). Scenarios: PoR events are ECL scripts read from the player's DAX files; the VM is decoded (`decode/ecl/ECL_VM.md`) but there is no script editor or override path. | **SOFTEN** → "A new rule or a changed screen is an edit, not a reverse-engineering project." (drop sprite and scenario until an override path exists) |
| V11 | SC "(SSI, 1988, QuickBASIC): 90 acceptance screens, 90 pass" | A3 | **KEEP** |
| V12 | SC "most of them pixel-compared against the original running in DOSBox" | A4: 64 of 90 compared (71%, so "most" holds) by pixel diff: 62 match apart from test data, 0 differ, 2 N/A. The claim log's "60/62" is the 10-16 count; current = 62 of 64. | **SOFTEN** (precision) → "90 acceptance screens, 90 pass; 64 were pixel-compared with the original running in DOSBox: 62 match apart from test data, none differ, 2 cannot be shown in the original." |
| V13 | SC "Mouse, gamepad, zoom, save slots, Classic mode …" | A5 | **KEEP** |
| V14 | PoR "(SSI, 1988, Turbo Pascal with overlays)" | `profiles/turbo-pascal-6`, PoR `BUILD_PLAN.md` | **KEEP** |
| V15 | PoR "105 screens tracked, 69 exact pixel matches, 25 differences with documented causes, the rest still being verified" | A6 | **SOFTEN** → "…, 8 not reached yet (overland map, endgame, a few rare events)." |
| V16 | PoR "It plays through" | A7 | **SOFTEN** → "Every town and dungeon area loads and plays in an automated sweep (29 of 29); the overland map and the endgame are not verified yet." |
| V17 | "neither game repo contains a byte of the original" | A9 | **SOFTEN** → "neither game repo contains the original's files: no program, data, graphics or sound (the decode notes quote game text as evidence)." |
| V18 | hash check, v1.3, local storage, never uploads | A10, A11, A13 | **KEEP** |
| V19 | "not clean-room; all rights … stay with their authors and publisher" | A14 | **KEEP** |
| V20 | Darklands "the overlay directory" | `profiles/microsoft-c-6/PROFILE.md` (resident offset 0x0BF7E); `cases/DARKLANDS_CHALLENGE.md` (task 2) states it | **KEEP** |
| V21 | "81 overlays" | same profile; challenge page | **KEEP** |
| V22 | "a working Ghidra export" | profile "Results so far": resident core + 81 overlays exported, ~4,400 functions, ~86% of bytes. The export itself is original-derived and is **not shared**; the challenge page gives the route, not the export. | **SOFTEN** (avoid implying a download) → "a proven route to a full Ghidra export". |
| V23 | "Microsoft C that decompiles cleanly" | profile: "decompiles well in Ghidra after the overlays are extracted" | **SOFTEN** → "Microsoft C 6 code that decompiles well". |
| V24 | "the two places where earlier attempts stalled" | Owner fact: two earlier attempts stalled. Public evidence names two stall causes: (1) the dynamic route reached ~21% code coverage (`METHOD.md:4`, profile); (2) a tool that saw only the 59 KB resident image and reads raw binaries as 32-bit code, so it could not read the 16-bit overlays (profile "Decompile notes"). `cases/DARKLANDS_CHALLENGE.md` names exactly these two. | **KEEP** |
| V25 | "Nobody has finished it." | no build exists (`CASES.md`, profile "No build attempted") | **KEEP** |
| V26 | "Pull requests, please. Decode work most of all: a new compiler profile, a new game case, a better tool, a fix to the method." | `CONTRIBUTING.md` (profiles, COMPATIBILITY rows, tools, METHOD/SCALING/templates); `.github/PULL_REQUEST_TEMPLATE.md`. `CASES.md`: game material never lives in this repo; a new case = a row + lessons, its decode in its own repo. | **SOFTEN** → "a new compiler profile, a link to your own game case, a better tool, a fix to the method." |
| V27 | "The contributing guide says what a PR must never contain (any original or original-derived bytes) and what it should (evidence for every claim)" | `CONTRIBUTING.md` "must never contain" (original files, extracts, decoded dumps, listings, pseudocode of copyrighted games; credentials, personal paths) + "Evidence rules". This is the **method repo's** rule; the two game repos contain original-derived pseudocode by design (ruling SC-3). | **SOFTEN** → "The method repo's contributing guide says what a PR must never contain (original files or anything extracted from them) and what it must have (evidence for every claim)." |
| V28 | Bug reports to each repo's Issues: screen, save, browser | A23 (templates, task 4) | **KEEP** |
| V29 | Disclaimer line | A25 | **KEEP** |
| V30 | Claim log "DOSBox reference count last known 60/62" | superseded: 62 REF PASS / 0 FAIL / 2 N/A of 64 (SC `STATUS.md:112`) | **FIX the log** before posting. |

## A. Announcement draft v2 (evidence rows)

| # | claim (v2 wording) | evidence | verdict / replacement |
|---|---|---|---|
| A1 | Title: "rebuilt as browser games from a full decode of the originals" | SC `DECODE_GATE.md:3` GATE MET 2026-10-15 (140/140 runtime routines, 7/7 modules rendered); PoR `DECODE_GATE.md:1` MET 2026-10-16 (10/10 items). Both gates are recorded with evidence. | **KEEP** |
| A2 | "Two SSI classics … rebuilt from a complete decode of the original DOS executables, not re-imagined" | as A1; PoR scope excludes only the third-party starter (`DECODE_GATE.md` "Known out-of-scope") | **KEEP** |
| A3 | SC "90 acceptance screens, 90 pass" | SC `ACCEPTANCE.md` summary block: all 90 / self-checked 90 / reviewed 90 / PASS 90 / FAIL 0 / open 0 | **KEEP**. Precise form: "90 acceptance screens, each checked by the builder and by an independent reviewer: 90 pass". (v1's "83" was the v1.0 count, `STATUS.md:228`.) |
| A4 | SC "the screens are checked against the original running in DOSBox, most of them pixel for pixel" | SC `STATUS.md:112` (dosbox-recompare 2026-10-18): **64** rows have a DOSBox reference: **62 REF PASS / 0 FAIL / 2 N/A** (SP-10, IN-04: no items, page cannot be shown in the original). `ACCEPTANCE.md` counts agree (62 REF PASS, 2 REF N/A). But REF PASS is **not** 0 px: `acceptance/ref/README.md` compare.py maps colours and counts mismatches; only **6** of the 62 are 0 px, the rest carry explained residuals (test-crew names, ship-class sprite of the fixture, dice rolls, star positions; e.g. 924 px "common residual" on SPACE screens, up to 14 593 px on IN-02). "Most of them pixel for pixel" is false. "60/62" was the 10-16 count. | **SOFTEN** → "64 of the 90 screens were compared with the original running in DOSBox: 62 match apart from test data (crew names, dice rolls), none differ, 2 cannot be shown in the original." |
| A5 | SC "Mouse, gamepad, zoom, help, save slots, and a Classic mode that switches every convenience off" | SC `game/README.md:84-174` (Mouse, Gamepad table, Map zoom F, Controls help F1/E, Named save slots L, Classic mode A); `game/engine/settings.js:2,24` Classic master switch; `game/engine/input.js` Gamepad API | **KEEP** |
| A6 | PoR "105 screens tracked: 69 match the original pixel for pixel, 25 differ for documented reasons, the rest are still being verified" | PoR `ACCEPTANCE.md:11-19`: 105 rows (cover all 106 SCREENS_INDEX ids) / **69 PASS** (= 0 differing px, exact RGB, line 4) / **25 DIFF** (25 explained, 0 real, 0 unresolved) / 1 NO-REF / 0 BLOCKED / 2 ERR-PATH / 8 pending. The 11 "rest" are not all "being verified": 2 ERR-PATH cannot occur in the browser (SU-01, SV-02), 1 NO-REF has no screen of its own (EV-12), 8 pending are not reached yet (overland AD-06/07, endgame EV-17, EV-04/10, CB-14, SY-03, EV-18). **Evidence gap:** PoR `ACCEPTANCE.md` links `acceptance/reports/` (per-shot SHA-256 + px counts) and `acceptance/acc/`, which the public filter did not keep; fixed in task 1 (see C1). | **SOFTEN** → "105 screens tracked: 69 match the original pixel for pixel, 25 differ for documented reasons, 8 are not reached yet (overland map, endgame and a few rare events)." |
| A7 | PoR "It plays through" | No full play-through on record. PoR `acceptance/integration/RUN-3.md` summary: 29/29 script areas reached with a level-4 test party, seeded 40-move walks, fights in 18, camp in 26, one crash found and fixed (#r3-1). RUN-1 (load, Phlan, save/reload) 13/13, RUN-2 (fight, camp, cast, temple, training, save) 5/5. Overland (AD-06) "not attempted yet", dragon finale (EV-17) pending. Open: #r2-2 (AC after combat). | **SOFTEN** → "Every town and dungeon area loads and plays in an automated sweep (29 of 29); the overland map and the endgame are not verified yet." |
| A8 | PoR "this one is the rougher alpha" | consistent with A6/A7 | **KEEP** |
| A9 | "Neither repo contains a byte of either game" | Gates PASS (SC `tools/byoc/public_check.mjs`, `docs/byoc/B6.md`; PoR `tools/public_gate.py`): no game files, data copies, graphics, sound, listings with raw bytes. But both trees **quote game text and short instruction encodings as evidence**: SC `docs/byoc/public_paths.md` "KEEP": pseudocode quoting game text (ruling SC-3), hex lines in *_VERIFY.md, `decode/data/MODULE_CONSTANTS.public.md`; PoR `docs/BYOC.md:26` "short literal strings (prompts …)" in `game/**/*.js`. "Not a byte" is literally false. | **SOFTEN** → "Neither repo contains the games' files: no program, data, graphics or sound. The decode notes quote game text where it serves as evidence." |
| A10 | "the browser asks for your own game folder, checks it by file hash" | SC `docs/byoc/manifest.json` (123 names + sizes + SHA-256, 115 required), `tools/byoc/import_check.mjs` 11/11 (`docs/byoc/B7.md` §2); PoR `game/byoc/manifest-por-1.3.json` (115 required, size + SHA-256), `README.md:10-13` | **KEEP** |
| A11 | "(Pool of Radiance needs version 1.3)" | PoR `game/byoc/manifest-por-1.3.json` id `por-1.3`; `README.md:13` other versions refused (ruling PR-4) | **KEEP**. Add for SC: the manifest knows exactly one release (`"version": "starcoma-1"`, the STARCOMA folder); other releases are untested and will be refused if any required file differs. |
| A12 | (dropped in v2) "GOG copies work" | No GOG copy was ever imported. The PoR reference copy's `POOL.CFG` was written by a third-party starter (PoR `docs/BYOC.md:42`, `DECODE_GATE.md` out-of-scope), so it is not a store release; whether GOG's PoR files hash-match v1.3 is **unknown**. SC: no evidence of a GOG release. | **DROP** stays dropped. If asked: "Store releases are untested; if yours is refused, open an issue with the importer's file list." |
| A13 | "keeps it in local browser storage, and never uploads anything" | SC: OPFS store (`docs/byoc/B7.md` §1, `game/byoc-sw.js`); PoR: IndexedDB `por-data` / `por-save` (`README.md:23-26`). Grep of `game/` for POST / sendBeacon / XMLHttpRequest: no hits; WebSocket only in test/screenshot tools (`misc.browser.mjs`, `*/shoot.mjs`, CDP), not loaded by the game. | **KEEP** |
| A14 | "built from an analysis of the original programs, not clean-room; all rights … stay with their authors and publisher" | Fixed position (owner); PoR `BUILD_PLAN.md:3`, `docs/BYOC.md:26` "direct translation … not clean-room" | **KEEP** |
| A15 | "The game logic is readable JavaScript, one module per original program module, with the decoded pseudocode and data specs next to it in the same repo" | **PoR:** `game/areas/*.js` committed, one file per area and per original overlay (`view_ov28.js`, `combat_ov05.js` …) with the `{seg:off}` address of each routine (`BUILD_PLAN.md:25`); pseudocode per area in `decode/pseudo/*.pas.md`, specs in `decode/data/*.md`. **SC:** pseudocode for all 7 programs in `decode/pseudo/*.bas.md`, but the JS of the five generated modules (space, inside, plbattle, spbattle, starport/flow) is **not in the repo**: it is produced in the browser from the player's own EXEs at import (tier 3, `docs/byoc/public_paths.md` REMOVE, `docs/byoc/B7.md` §1). The repo holds the translator (`game/byoc/bas2js.js`, `qb2bas.js`), the engine and the hand-written `startup.js`. | **SOFTEN** → "The game logic is readable JavaScript organised like the original program, every routine tagged with its original address, and the decoded pseudocode and data specs are in the same repo. (Star Command translates its program modules in your browser from your own copy; Pool of Radiance ships them.)" |
| A16 | "Changing a rule, a screen or a sprite is an edit, not a reverse-engineering project" | PoR: edit `game/areas/*.js`. SC: a JS file placed in `game/modules/` is served before the imported one (`docs/byoc/B7.md` §1, byoc-sw: network first, OPFS only on 404), so a modder exports the generated module, edits it and drops it in; sprites are rebuilt from the player's banks, so "a sprite" means an override, not a file in the repo. Neither README documents this yet (task 1 adds it). | **SOFTEN** → "Changing a rule or a screen is an edit, not a reverse-engineering project." (drop "or a sprite" until an override path is documented) |
| A17 | "a half-day gate test tells you whether a game is suitable" | `METHOD.md` §Phase 0 (gate test) | **KEEP** |
| A18 | pipeline list (static whole-program disassembly … DOSBox pixel oracle … translation into an engine) | `METHOD.md` phases; both case trees: listings/pseudo, *_VERIFY.md, DOSBox refs, engines | **KEEP** |
| A19 | "Proven on a QuickBASIC game and a Turbo Pascal game" | `COMPATIBILITY.md`, `profiles/quickbasic-3`, `profiles/turbo-pascal-6`; both games built to alpha | **KEEP** |
| A20 | "a threaded-Forth one (Starflight 2) is being decoded now" | assignment situation: decode started 2026-10-18, private repo `Starflight2RE`; no public evidence | **KEEP** as worded (no more than "being decoded"). |
| A21 | "**Darklands** is posted as an open challenge with everything known so far" | becomes true with `cases/DARKLANDS_CHALLENGE.md` (task 2) | **KEEP** once task 2 is committed. |
| A22 | Links: `DrEvil-TitaniumHelix/star-command-remake`, `pool-of-radiance-remake`, `remaster-dos-games` | RL-1 = A (2026-10-18). The two game repos do not exist on GitHub yet; `remaster-dos-games` exists but is private. | **KEEP** (valid only after the release commands run and the repos are public). |
| A23 | "Bug reports go to each repo's Issues: name the screen, attach a save, say which browser" | issue templates added in task 4 (`.github/ISSUE_TEMPLATE/`) | **KEEP** once task 4 is committed. |
| A24 | "'The original did this too' … gets its own label" | label must be created at release (`tools/release.py` step f, `RELEASE.md` (j)) | **KEEP** once the label exists. |
| A25 | Disclaimer line | owner's fixed wording | **KEEP** |

## B. Star Command public README (`README.md`, `game/README.md`)

| # | claim | evidence | verdict / replacement |
|---|---|---|---|
| B1 | root `README.md:1-3` "Star Command RE (REA process test)" | internal working title | **DROP**: README rewritten for players (task 1). |
| B2 | root `README.md:10` a local path to the original files on the build machine | machine detail | **DROP** (scrub, task 1). |
| B3 | root `README.md:13` "private repo … remaster-dos-games, method commit a89f296" | repo goes public; a89f296 will not exist on GitHub (RL-2: fresh commit) | **SOFTEN** → "Built with Remaster DOS Games (https://github.com/DrEvil-TitaniumHelix/remaster-dos-games), method version v0.1.0." |
| B4 | `game/README.md:5` "Your saved game uses the original save file format" | `game/README.md:182` save = the original `CHARINFO.BAS`; `docs/byoc/B7.md` §2 veteran save from OPFS = committed CHARINFO.BAS byte-equal | **KEEP** |
| B5 | `game/README.md:9` "Classic mode … then you play the original exactly" | `settings.js` master switch; acceptance shots are taken with additions idle (`game/README.md:243`) | **SOFTEN** → "Classic mode switches all of them off at once, for the original game as checked by the acceptance screens." ("exactly" overstates: 2 open DOSBox questions, D-IN-3, D-MX-2) |
| B6 | `game/README.md:11-60` launcher tied to one handheld PC, its user folder and Python path | machine-specific | **DROP** (rewrite Run section generically: `python -I tools/serve.py 8088`, any static server; task 1). |
| B7 | `game/README.md:96-119` gamepad table named after one handheld's built-in controls | `input.js` standard Gamepad API mapping | **SOFTEN** → "Gamepad (standard layout, e.g. Xbox-style)": same table, button names A/B/X/Y/LB/RB/Start/View. |
| B8 | `game/README.md:168` "in 59 places where the rule book is wrong" | `decode/docs/MANUAL_XCHECK.md`: 60 DISCREPANCY (`DECODE_GATE.md:37`); the Manual button reads `manual.json`, which is not in the public tree (`public_paths.md` REMOVE; commit 34203a6 "manual.js degrades when manual.json is absent") | **SOFTEN** → in the public build the Manual button has no rule-book text (the manual is not distributed); state that, keep the "what the game really does" notes only if they ship. Mark as known limitation. |
| B9 | `game/README.md:190-204` veteran crew "Details: `assets/saves/veteran/README.md`" | removed from public tree (`public_paths.md`); the importer rebuilds the save (`convert/veteran.js`) | **SOFTEN**: keep the feature, drop the link. |
| B10 | `game/README.md:231-235` "90 screens … all 90 pass"; "64 screens compared: 62 match, none differ, 2 could not be shown" | as A3/A4 | **KEEP** (add "apart from test data"). |
| B11 | `game/README.md:236` "More than 13 questions … answered with DOSBox" | `acceptance/DOSBOX_REQUESTS.md`, `STATUS.md:313` "13+ DOSBox questions settled" | **KEEP** |
| B12 | Known gaps D-IN-3, D-MX-2, beam flash | `game/README.md:241-247`, `STATUS.md:103,129` | **KEEP** (beam flash: REF N/A, `STATUS.md:115`). |
| B13 | `?screen=` dev jumps "load the shipped save" | in the public build the save comes from the import | **SOFTEN** → "load the original save from your imported copy". |

## C. Pool of Radiance public README (`README.md`)

| # | claim | evidence | verdict / replacement |
|---|---|---|---|
| C1 | (implicit) acceptance evidence in the repo | `ACCEPTANCE.md` links `acceptance/reports/` (82 JSON: keys, SHA-256 of shot and reference, differing px), `acceptance/acc/` (gen.py, run_at.mjs, runs/*.json), `acceptance/paths.*`, `acceptance/ref/<id>.capture.json`: **none are in the public tree** (`tools/make_public_repo.py` ALLOW list lacks them). Also `DECODE_GATE.md:14` cites `acceptance/ref/DECODE_CHECKS.md`. | **FIX** in task 1: add the text-only evidence files (no PNGs) to the public tree and the public copy of the allow-list; re-run `public_gate.py`. |
| C2 | `README.md:1-3` "Pool of Radiance RE / Trial of the Star Command method …" + a local user path to the originals | internal, machine path | **DROP** (rewrite, task 1). |
| C3 | `README.md:6` "private repo … method commit a89f296" | as B3 | **SOFTEN** as B3. |
| C4 | `README.md:10-13` v1.3, `START.EXE`, `ITEMS`, 113 `.DAX`; others refused (PR-4) | `manifest-por-1.3.json` (115 required files) | **KEEP** |
| C5 | `README.md:14` Chrome/Edge folder picker; others pick or drop files | `game/byoc/ui`, `engine/byoc.js` collectFromDirectoryHandle / FileList / DataTransfer (`game/README.md:51`) | **KEEP** |
| C6 | `README.md:17` `python -I tools/serve.py 8188 --player` | `tools/serve.py` in tree | **KEEP** |
| C7 | `README.md:23-26` IndexedDB `por-data` / `por-save`, gear button, saves ZIP export | `README.md`, BY-5 commit bdac239, `engine/files.js` | **KEEP** |
| C8 | `README.md:29-34` keyboard / gamepad / mouse | `engine/input.js:124-138` (buttons 2/3 = X/Y rotate menu highlight), `BUILD_PLAN.md:17` | **KEEP** |
| C9 | `README.md:35` code wheel check skipped (`?wheel=1` shows it) | `BUILD_PLAN.md:25` | **KEEP** |
| C10 | `README.md:37-40` the owner's desktop shortcuts | personal, machine-specific; the .cmd files are not in the tree | **DROP** |
| C11 | v1 claim "the party transfer files are the originals' format" | `BUILD_PLAN.md:21` files.js writes SAVE/ formats (CHRDAT*.SAV/.ITM/.SPC, SAVGAM*.DAT) and `docs/BYOC.md:79` size-checks imported saves; RUN-1 save/reload round trip in the **port** only. No test that an original-program save loads in the port or a port save loads in DOS, and no test of a transfer into the sequel. | **DROP** stays dropped. Safe form if wanted: "Saves are written in the original SAVE file layout; loading them in the DOS game is untested." |
| C12 | PoR gamepad (v1 "gamepad on both") | C8 | **KEEP** |

## D. Points for the owner (not claims, found during the audit)

1. **Provenance wording: RESOLVED (owner 16:55) = removed** from both public trees; game-source names are now a hard pattern in `tools/personal_gate.py`.
2. **Personal-data gate**: 0 hits in both public trees after task 1 (STATUS.md, task 1 block).

## E. v4 with the replacements applied (for the coordinator / the owner to edit)

**Title:** Remaster DOS Games: recode a DOS game, mod it, play it. First two examples: Star Command and Pool of Radiance (SSI, 1988), alpha. Pull requests wanted.

Three things you can do with this, in one open toolkit:

**1. Recode a DOS game.** A documented method takes an old DOS game from "nothing" to a decoded, verified, playable rebuild. It works because many 1980s compilers were naive: their machine code maps almost one to one back to source. Account for every byte of code, name the language runtime once, read each module as the program it was. A half-day gate test tells you whether your game is suitable before you spend much. Then: static whole-program disassembly, per-module pseudocode, independent verification, a DOSBox pixel oracle, translation into a browser engine. Method, tools, templates and two worked cases: https://github.com/DrEvil-TitaniumHelix/remaster-dos-games

**2. Mod a DOS game.** Once a game is recoded, its logic is readable JavaScript organised like the original program, every routine tagged with its original address, with the decoded pseudocode and data specs beside it. A new rule or a changed screen is an edit, not a reverse-engineering project.

**3. Play the two examples**, in a browser, alpha:
- **Star Command** (SSI, 1988, QuickBASIC): 90 acceptance screens, 90 pass; 64 were pixel-compared with the original running in DOSBox: 62 match apart from test data, none differ, 2 cannot be shown in the original. Mouse, gamepad, zoom, save slots, and a Classic mode that switches every convenience off. https://github.com/DrEvil-TitaniumHelix/star-command-remake
- **Pool of Radiance** (SSI, 1988, Turbo Pascal with overlays): 105 screens tracked, 69 exact pixel matches, 25 differences with documented causes, 8 not reached yet. Every town and dungeon area loads and plays in an automated sweep; the overland map and the endgame are not verified yet. This is the rougher alpha. https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake

Bring your own copy: neither game repo contains the original's files (no program, data, graphics or sound). On first start the browser asks for your own game folder, checks it by file hash (Pool of Radiance needs version 1.3; store releases are untested), keeps it in local browser storage, and never uploads anything. The engines come from an analysis of the original programs, not clean-room; all rights to the games stay with their authors and publisher.

**Try Darklands.** Everything known so far is posted as an open challenge: the overlay directory, 81 overlays, a proven route to a full Ghidra export, Microsoft C 6 code that decompiles well, and the two places where earlier attempts stalled. Nobody has finished it. Have a go.

**Pull requests, please.** Decode work most of all: a new compiler profile, a link to your own game case, a better tool, a fix to the method. The method repo's contributing guide says what a PR must never contain (original files or anything extracted from them) and what it must have (evidence for every claim). Bug reports go to each repo's Issues: name the screen, attach a save if you have one, say which browser.

Disclaimer: all or part of this post may have been written or edited by super intelligence
