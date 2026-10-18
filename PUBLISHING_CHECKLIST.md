# Before this repo goes public (owner decides; nothing is pushed until he says so)

1. **License**: DECIDED (owner, 2026-10-16) = MIT for code + CC BY 4.0 for docs (LICENSE, LICENSE-MIT, LICENSE-DOCS). Copyright holder: DrEvil and Titanium Helix LLC (owner, 2026-10-16).
2. **Scrub personal and machine details** in METHOD.md, README.md, SCALING.md, templates/ and cases/: owner name, user home paths, machine names, the coordinator persona, network addresses. Replace with neutral roles ("owner", "coordinator session") and placeholders (`<repo>`, `<targets>`).
3. **cases/**: keep the lessons, drop or trim game-specific internals (offsets beyond short evidence, function names of copyrighted games). The two Foreman memories are working logs; publish condensed versions or none.
4. **templates/**: the Foreman examples name real game folders and decisions; turn them into generic templates with one short worked example each.
5. Make the "never contain" list in CONTRIBUTING.md true for the repo itself.
6. Repo name, owner account and description; README badge-free and factual (no "almost any DOS game" claim until COMPATIBILITY.md supports it).
7. Owner's explicit "send it" before the first push.

## Status 2026-10-16
- Items 2-5 DONE: names, user paths, machine names, coordinator persona and network addresses replaced with roles and placeholders; raw Foreman logs and the full Fable report removed from cases/ and replaced with LESSONS.md and FABLE_SPOTCHECK_SUMMARY.md.
- Repo name: **Remaster DOS Games** (GitHub slug `remaster-dos-games`), owner account to be confirmed at publish time.
- **New item 8: publish with a fresh history.** Earlier local commits still contain the raw logs and personal paths. Before the first push, create a single clean initial commit (orphan branch) so none of that history leaves this machine.
- HOLD: owner will not publish until Star Command and Pool of Radiance are confirmed working by him.

## Status 2026-10-18 (release lane)
- HOLD lifted: the owner tested both games ("alpha, ready for community testing").
- Item 6 DONE: README rewritten by audience (recode / mod / play, Darklands challenge, pull requests); "any DOS game" is
  the owner's heading, with the gate-test and compatibility caveat in the body.
- Item 8 confirmed (ruling RL-2 = A): this repo and both game repos are published as one clean initial commit each,
  authored by the public persona's no-reply address (`RELEASE.md`, hard rule); `herdr/` and `STATUS.md` are excluded.
- Personal-data gate: `tools/personal_gate.py` (generic patterns here, the owner's own patterns in a private file outside
  the repo); 0 hits required before any publish.
- Item 7 still open: the owner's explicit "send it".
