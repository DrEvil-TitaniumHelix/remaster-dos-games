# Case studies — the games this method was developed on

Each game lives in **its own repository**, never inside this one. Game repos hold game-derived material (pseudocode,
decoded data descriptions, rebuild code that reads the original files) and are published, if at all, under their own
rules: bring your own copy, no original bytes (`RELEASE.md`). This repo links to them and keeps only the lessons.

| Game | Original toolchain | Outcome | Case repo | Profile |
|---|---|---|---|---|
| Star Command (SSI, 1988) | QuickBASIC 3 + BRUN30 | **alpha release v0.1.0**: decode gate ~9 h; playable v1 overnight; 90/90 acceptance screens, 62 of 64 DOSBox comparisons match (2 cannot be shown); QoL additions with a Classic mode | [star-command-remake](https://github.com/DrEvil-TitaniumHelix/star-command-remake) | `profiles/quickbasic-3` |
| Pool of Radiance (SSI, 1988) | Turbo Pascal 6 + FBOV overlays, EXEPACK | **alpha release v0.1.0**: decode gate ~5-6 h on Opus + Codex; Fable spot-check 90% exact; 69 of 105 screens pixel-exact, 25 documented differences, 8 pending; overland map and endgame not verified | [pool-of-radiance-remake](https://github.com/DrEvil-TitaniumHelix/pool-of-radiance-remake) | `profiles/turbo-pascal-6` |
| Starflight 2 (Binary Systems, 1989) | threaded Forth | **in progress** (threaded Forth, gate test running) | private | — |
| Darklands (MicroProse, 1992) | Microsoft C 6 + PKWARE-imploded overlays | earlier dynamic attempts stalled (~21% coverage); the static overlay route then decoded most areas before work was stopped by choice; no build. **Open challenge:** [cases/DARKLANDS_CHALLENGE.md](cases/DARKLANDS_CHALLENGE.md) | private | `profiles/microsoft-c-6` |

## How the repos link
- **Method to cases:** this table, plus each profile's "Proven on" line.
- **Cases to method:** each case repo's README carries a "Built with Remaster DOS Games" line naming this repo and the
  method version it followed, and its `FOREMAN.md` points at `METHOD.md` instead of copying the rules.
- **Lessons flow upstream:** when a case run hits a new trap or finds a better tool, the fix lands here (METHOD.md
  traps, a profile, or `tools/`) in a separate commit, with no game content.
- **Your own case:** add a row by pull request with a link to your repo and the profile it used.
- Not git submodules: the method must stay publishable on its own, independent of any game repo.
