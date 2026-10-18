# RELEASE — from a private decode workspace to a public game repo

The repeatable process behind the first release (Star Command and Pool of Radiance, v0.1.0-alpha, 2026-10-18). It
applies to every game repo and, where marked, to this method repo. The script is `tools/release.py`; it dry-runs by
default and prints every command before it runs one.

## Hard rules
1. **Public identity only.** Every published commit is authored *and* committed by
   `DrEvil <ID+DrEvil-TitaniumHelix@users.noreply.github.com>` (ID from `gh api user --jq .id`), set repo-locally in the
   clean tree; never the owner's personal name or e-mail. Commit messages keep the `Co-Authored-By: Claude ...` trailer.
   `release.py publish` refuses any other author or committer.
2. **One clean commit per public repo** (ruling RL-2): the working history never leaves the machine. The filtered
   clones stay local; the published repo is a new directory with one initial commit and the version tag.
3. **Personal-data gate: zero hits.** `python -I tools/personal_gate.py <tree>`: user paths, network addresses,
   session and pane ids, host names, phone numbers, street addresses, e-mail addresses, names of sites games were
   obtained from, plus the owner's own patterns (names, accounts, machines, persona) from a private file outside every
   repo. Game text that happens to match goes into the tree's `.personal-gate-allow` with a reason.
4. **No original bytes, ever** (bring your own copy): the game repo's own gate must PASS on the tree and its history.
   Never name where a copy of a game came from.
5. **Nothing touches GitHub until the owner says "send it"**, per repo. Lanes only dry-run.
6. **No GitHub Pages** (ruling RL-3 = B): players download and serve locally.
7. This repo's public commit excludes `herdr/` (lane files) and `STATUS.md` (lane log).

## Steps per game repo
**(a) Private workspace → filtered public clone.** An allow-list of own-work paths (engine, importer, translators,
pseudocode, specs, tools, docs) applied with `git filter-repo` to a clone; the private workspace is never modified. A
new game must provide a pair: a **filter** (allow-list or deny-list) and a **gate** that proves the result holds no
original bytes, in the tree and in every blob of the history. The two existing pairs:
- Pool of Radiance: `tools/make_public_repo.py` (allow-list + deny pass) + `tools/public_gate.py` (forbidden paths,
  SHA-256 of every original file and decoded record, binary runs ≥ 31 bytes, hex dumps; game text reported only).
- Star Command: `tools/byoc/public_filter.txt` (`git filter-repo --paths-from-file … --invert-paths`) +
  `tools/byoc/leak_scan.py` (`<tree>` and `--history`: hash, binary runs ≥ 32 bytes; text and game strings reported),
  plus a playability check from the private workspace (fresh browser profile imports a real copy and reaches the
  first screens).

**(b) Scrub pass + README standard.** Personal and machine details out (rule 3), copy provenance out (rule 4). The
README follows one order: **Play** (what you need = your own copy and which version, how to start with
`python -I tools/serve.py <port>` or any static server, where saves live, controls including gamepad, known alpha
limitations, how to report), **Modify** (engine, game logic, how to change a rule or a screen, how acceptance works),
**Decode** (what the decode folders are, evidence rules), a "Built with Remaster DOS Games" line with the method
version, **Credits and licence** (original authors and publisher named plainly, DrEvil, MIT + CC BY 4.0 for own work
only), the one BYOC/IP sentence ("contains no original game files; derived from analysis of the original program, not
clean-room"), and the line "Disclaimer: all or part of this repository may have been written or edited by super
intelligence".

**(b2) Clean tree** (rule 2): `python -I tools/release.py clean <clone> ../<repo-name> --version vX.Y.Z-alpha --run`
copies the clone's tracked files at HEAD into a new directory, `git init`, one commit, annotated tag.

**(c) Gates PASS, recorded.** In the clean tree: the game's own gate, the personal-data gate, a clean work tree. Record
the result in the workspace's STATUS log (counts, not content).

**(d) Version + changelog.** Tag `vX.Y.Z-alpha | -beta | -rc.N` (created by step b2). `CHANGELOG.md` has a
`## vX.Y.Z-…` section: what plays, what is known broken (the open rows of `ACCEPTANCE.md`), what BYOC requires (which
version, which files).

**(e) GitHub repo.** `gh repo create <owner>/<name> --public --source . --remote origin --push`, then push the tag.

**(f) GitHub Release.** Notes = the CHANGELOG section; asset = a zip of `game/`, `tools/serve.py`, README, CHANGELOG
and licences for players who do not use git; `--prerelease` for alpha/beta/rc. Create the label
**"original did this too"**.

Steps (c)-(f) in one command: `python -I tools/release.py publish ../<repo-name> --repo <owner>/<name> --version <tag>
--gate "<the game's own gate>" [--push]`. Without `--push` it runs the gates and prints the GitHub commands only.

**(g)** — dropped (RL-3 = B: no Pages).

**(h) Link the method.** This repo's `CASES.md` row (repo link, outcome = the released version), and the game README's
"Built with Remaster DOS Games … method version vX.Y.Z" line.

**(i) Announcement checklist.** Post text in `docs/announcements/` audited claim by claim (`CLAIMS.md`: every number
traced to a file in the public tree; KEEP / SOFTEN / DROP); disclaimer line "Disclaimer: all or part of this post may
have been written or edited by super intelligence"; screenshots only from outside every repo; **the owner posts**.

**(j) Feedback intake.** `.github/ISSUE_TEMPLATE/` in each game repo: a bug template asking for the screen (name or
acceptance id), a save, the browser and version, and whether the original does the same; the "original did this too"
label for confirmed original behaviour.

## This method repo
Same rules 1-5 and 7: `release.py clean . ../remaster-dos-games-public --version v0.1.0 --exclude herdr --exclude
STATUS.md --run`, then `release.py publish ../remaster-dos-games-public --repo DrEvil-TitaniumHelix/remaster-dos-games
--version v0.1.0 --no-zip --existing`. The GitHub repo already exists (private, with an earlier commit by the owner's
personal identity), so `--existing` replaces `gh repo create` with: add the remote, `git push --force origin main` (the
clean commit replaces the old history), and `gh repo edit … --visibility public --accept-visibility-change-consequences`.
Both are irreversible in effect and run only with the owner's explicit approval.

See `ARCHITECTURE.md` for how the decode and build behind a release are run.
