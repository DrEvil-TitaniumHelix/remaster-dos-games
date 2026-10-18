# ARCHITECTURE — what gets built, and how the agents run

Two things matter most: what comes out is a **plain JavaScript game on an HTML5 canvas**, and what produces it is an
**adaptable agent graph in Herdr**. Everything below is from `METHOD.md`, `SCALING.md` and `cases/LESSONS.md`.

## 1. The output: plain JavaScript on an HTML5 canvas

- Each rebuilt game is `index.html` plus vanilla ES modules: **no framework, no bundler, no build step**. It draws into a
  canvas at the original resolution (320×200, EGA palette), scaled in whole steps; input is keyboard, mouse and the
  browser Gamepad API. Any static web server runs it (both games ship a small Python `tools/serve.py`).
- The game logic is the decoded program translated routine by routine, each routine tagged with the original address,
  so a modder reads JavaScript and can trace any line back to the pseudocode and the bytes.
- The decode side is **Python + Ghidra** (headless, one instance at a time), plus small Python tools in `tools/`
  (MZ parser, 16-bit disassembler, EXEPACK unpacker, Turbo Pascal overlay splitter). The oracle is DOSBox-X, run headless.

## 2. The engine of the method: an adaptable agent graph in Herdr

[Herdr](https://herdr.dev) is a terminal workspace manager for coding agents (version used: 0.9.5). It runs each
agent in its own pane and lets one agent start, message, wait for and stop others.

- **One persistent Foreman per game repo** plans the work, writes one assignment file per lane, routes fix requests,
  enforces the decode gate and keeps its own memory file. It restarts from the files, never from chat.
- **Lanes are started, reused and closed per phase**: survey, toolchain identification, runtime naming, data formats,
  per-module decode drafts, finals, independent verification, build (engine, then one lane per area), QA, the DOSBox
  oracle. The graph is **not fixed in advance**: the Foreman reshapes it from what the repo files say (`STATUS.md`,
  assignments, fix and review requests).
- **Everything between agents goes through files in the repo**: one owner per file, a commit per result, a
  `STATUS.md` block per lane. Any lane, or the Foreman itself, can crash, hit a usage limit or be replaced mid-run and
  the next one resumes from the files.
- A **coordinator session** above the Foremen only relays the owner's rulings and watches milestones; it does no lane
  work.

## 3. Models and billing: three flat-rate subscriptions in fixed roles

No per-token API billing anywhere; three subscriptions at their top tier.

| Provider | Model | Role |
|---|---|---|
| Anthropic | Claude Opus | Foreman, decode finals, tooling, verification, build |
| Anthropic | Claude Fable | bounded spot-check only (e.g. 30 routines + 8 opcodes + 3 formulas, about 1% of a weekly budget) |
| OpenAI | Codex | bulk first drafts: pseudocode per area, data drafts, build drafts (1-2 sentence prompts that point at files) |
| Z.ai | GLM | independent review by a different model |

Any of the three can be dropped and its role moved to another: Star Command's last GLM review waited for a quota reset
while Opus verification carried the decode gate, and Pool of Radiance was decoded on Opus + Codex alone (no GLM lane);
Opus can also write the first drafts when Codex is unavailable, at the cost of its own budget. The model is not the key ingredient; the near-source machine code is
(`METHOD.md`, "Why this works").

## 4. Memory limits

- About **1.5 GB of RAM per working lane** (measured about 1 GB all-in: the agent process about 0.3 GB, the rest its
  headless Chrome, Python and test servers), plus fixed reserves: the OS and your apps (6 GB small machine, about 16 GB
  big one), **one Ghidra headless at a time** (4 GB Java heap), **one WSL + DOSBox-X oracle at a time** (2-4 GB), and
  **one browser under test at a time**.
- Lanes = min(RAM limit, CPU limit): RAM limit = (RAM − OS − Ghidra − oracle) / 1.5; CPU limit = about 1 build/test
  lane per physical core or about 2 decode lanes per core.
- 16 GB handheld, 8 cores: (16−6−4−2)/1.5 = about 3-4 heavy lanes, about 6 mostly-decode lanes. Measured overload with
  about 11 lanes: 0.3 GB free, 100% CPU, a lane watcher killed for low memory.
- 128 GB desktop, 16+ cores: (128−16−4−6)/1.5 = about 65 by RAM, but 12-16 recommended (work shape, Foreman span,
  usage budget).

## 5. Lane suggestions

| Machine | Lanes, Foreman included |
|---|---|
| 16 GB laptop or handheld | about 6 (the owner's hard cap on the handheld after a 12-lane overload) |
| 32 GB | about 10 (by the formula above; not measured) |
| 64-128 GB desktop | 12-16, with sub-foremen per area group past about 8 lanes |

| Phase | Useful lanes |
|---|---|
| 0. Gate test (half a day) | 3-4: survey, toolchain/packing, one-layer search, one data format |
| Decode | one draft lane per module or area group + one independent verifier (Star Command: 7 modules; Pool of Radiance: 6 areas) |
| Build | one engine lane + one lane per area + QA + the DOSBox oracle lane |

More lanes than independent modules only adds collisions on shared globals and the same pseudocode file, and past
about 8 lanes the Foreman becomes the bottleneck (`SCALING.md` §3-4).
