# Changelog

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
