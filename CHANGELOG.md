# Changelog

## v0.2.3 — 2026-10-28 (the full playthrough as a reusable component)
- METHOD.md: THE FIRST RULE: a title is not built until an AI has played it start to finish through the engine's play API (decisions as data, snapshot anywhere).
- docs/PLAYTHROUGH.md: the pre-release verification component: plan from the decode, specialist planners per game domain (derived at kickoff), one schema, one model-free executor with per-domain policies, the blocker loop with guards, the deterministic speedrun gate, the typical-state rule, sources, measured model mix, middle-title pilot then roll-out. METHOD.md Acceptance points to it.
- docs/PLAYTHROUGH.md §2a/§2b (from the Gold Box pilot): capability negotiation as a plan-time blocker; a published per-domain action vocabulary as the planner contract, prose only in `why`, static plan-vs-vocabulary check before any live run.
- docs/PLAYTHROUGH.md §2c: cross-domain requests as first-class plan data with id, owner and state; the static check fails on open requests and orphans (stops or fights no route step plays, preconditions nothing produces). Requests carry a scope (checkpoint / chapter); checks block only on requests due at or before the segment run; the plan converges chapter by chapter.
- docs/PLAYTHROUGH.md §3: the typical state is played by a good player (all buffs, all upgrades); only a loss with them is a finding.
- docs/PLAYTHROUGH.md §3: the state is as strong as reasonably possible before every mandatory obstacle (all reachable XP, training, gear, consumables); the plan is the strong-player route, then speedrun that route. Grinding to a per-obstacle level target is part of the plan; the executor provides a grind primitive. Grinding is bounded: content first, then at most three fights per chapter at the best spot; an unmet target is lowered, not ground out. The plan carries a human fight budget of about three times the scripted fights (SSB: 49 scripted, ~150 total, ~20 h). The route is completionist: all side quests and optional content by the finale; deferred, never skipped. Plan shape = the loop: staging side quests -> campaign fight -> next (owner). The run is always running; fix forward from blockers. Blocker loop in batch mode: collect every blocker per chapter, fix in parallel, replay once.
- docs/PLAYTHROUGH.md §1c (owner): two testing lanes: coverage in cheat mode (fights auto-won, debug only) and each scripted fight tested on its own in the harness.
- docs/PLAYTHROUGH.md §1b (owner, the pivot): the plan is made by a live model-in-the-loop player walking the walkthrough one step at a time; the recorded trace is the plan; its model-free replay is the gate. Specialists become on-demand helpers. Retry loop: three attempts, then level, then three more. An apparently impossible obstacle: all available side quests first, then return. Side content gets strength targets too, ordered and deferred by required strength. Targets are bounded by decoded attainable ceilings.
- docs/PLAYTHROUGH.md §4: the game's manual, rule book and journal are read first, before any plan; documented mechanics are never discovered by losing to them. A knowledge lane writes KNOWLEDGE.md (manual + guides, cited) before any plan step; the executor gets a sanity module from it; the standard is better than a human.
- docs/PLAYTHROUGH.md §1a: a persistent Strategy Expert (cross-game knowledge from reading and from play) and a Player Expert that consults it and directs the domain specialists; the executor stays model-free. Thrash escalation: specialist -> Strategy Expert -> targeted online research of the stuck event -> owner; never a third blind attempt. Required strength comes first from the guides (cited), then is predicted per obstacle from the decoded encounter (a per-engine estimator); over-preparation is the shortest path. Obstacles may be test-run in isolation with synthetic states to find the winning level; the playthrough earns that level by play. Tactics always best, never a substitute for level; a loss below target is a progression bug, not a tactics bug.

## v0.2.2 — 2026-10-24 (full playthrough = the third verification workflow and the pre-release gate)
- METHOD.md Acceptance: three verification workflows (bot trials; the optional DOSBox oracle; the full playthrough). The full playthrough is derived from the decoded scripts by a plan lane, played by the bot end to end on the virtual clock, doubles as the generated player walkthrough, and is required before any release is called complete.

## v0.2.1 — 2026-10-21 (acceptance revision: the remake plays itself; the oracle is optional)
- METHOD.md: new **Acceptance** section (owner ruling 2026-10-21). Success is defined by the remake, not the emulator: (1) internal playability = an autoplay bot drives the reproduction through every reachable area and script, fights, saves and reloads under node, failing on any error or non-round-tripping save; (2) save-file swap = data layouts proven against saves the original wrote. Behavioural correctness comes from the decode verify, then the owner plays.
- Rigor is per engine, not per game: the first title on an engine gets the full method; follow-up titles verify the engine delta and ship.
- The DOSBox-X oracle is now **optional, chosen at kickoff** (Phase 0 ruling, default internal): none / minimal (one short save-byte compare) / medium (spot screens + run-throughs) / complete (full per-screen table). Never a keystroke replay of a long recorded walk. Phase 3 and the oracle section rewritten accordingly.

## v0.2.0 — 2026-10-20 (method revision 2, Plus layer, Darklands fulfilled)

- **Plus layer standard:** Phase 6 is now the standard quality-of-life package (`docs/PLUS_LAYER.md`): three layers,
  the hook contract, fourteen packages with gates, order, lanes and traps; first built in one day as Gold Box Plus on
  the Pool of Radiance remake (original game 70/70 rows at 0 px with everything mounted). Star Command is the second
  implementation (trial of what is shared); Darklands follows.
- **METHOD revision 2:** the pathway now asks two questions in order: *can we reproduce it* (static recompilation of
  the whole executable over an emulated real-mode memory, services emulated at a high level, playable from day one)
  and only then *can we recode it* (modules replaced one at a time behind switches). Suitability rules rewritten:
  compiler quality and the "one layer" are now cost factors, not requirements; new D6 (an existing reproduction under
  a usable licence means fork with credit); prior-art search is the first step of the gate test; the oracle is built in
  as lock-step play. Product form: native SDL build; HTML5 only as the optional final phase.
- **Darklands challenge fulfilled** by [Darklands+](https://github.com/bouchacha/Darklands-plus) (bouchacha, MIT),
  verified on our own copy. `CASES.md`, `README.md`, `COMPATIBILITY.md`, `profiles/microsoft-c-6` and `cases/DARKLANDS_CHALLENGE.md` updated; the challenge page is
  kept as the record of why decoding alone could not finish it.
- Analysis of why that route succeeded where ours failed: `docs/DARKLANDS_PLUS_ANALYSIS.md`.

## v0.1.0 — 2026-10-18 (first public release)

- **Method** (`METHOD.md`): principles, suitability rules, the half-day gate test, phases and gates, roles, file
  protocol, traps already paid for.
- **Architecture and scaling** (`ARCHITECTURE.md`, `SCALING.md`): plain JavaScript / HTML5 canvas output; the Herdr
  agent graph with one persistent Foreman per game; model roles; memory limits and lane counts per machine and phase.
- **Compatibility** (`COMPATIBILITY.md`, `profiles/`): QuickBASIC 3 (oracle-verified), Turbo Pascal 6 + overlays
  (decoded, alpha build), Microsoft C 6 + imploded overlays (decoded in part).
- **Templates** (`templates/`): Foreman briefs, decode gate, build plan, lane assignments, each with a worked example.
- **Tools** (`tools/`): DOS MZ parser, 16-bit disassembler, EXEPACK unpacker, Turbo Pascal overlay splitter, context
  grepper, personal-data gate, release script.
- **Release process** (`RELEASE.md`): private workspace to public game repo, gates, one clean commit, BYOC.
- **Cases** (`CASES.md`, `cases/`): Star Command and Pool of Radiance released as v0.1.0-alpha; Starflight 2 in
  progress; the Darklands open challenge.
