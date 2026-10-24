# SCALING — how many lanes, and why not 12 or 24

Six lanes was not magic. It was the most the work and the machine could use at once. More lanes only help when all four limits below allow it.

## 1. The machine (the hard limit on a 16 GB handheld)
Measured on the 16 GB handheld PC, 2026-10-16 ~12:20 MDT, with ~11 agent lanes alive across two projects:

| Resource | Value |
|---|---|
| RAM visible to Windows | 15.7 GB |
| RAM free | 0.3 GB |
| CPU load | 100% |
| Claude processes | 19, 3.3 GB |

Each Claude lane is a node process plus its tools; build/acceptance lanes also run headless Chrome; Ghidra needs several GB of Java heap; DOSBox-X runs in WSL. Star Command already lost a lane watcher to a low-memory kill. **the handheld tops out around 6-8 active lanes.** The main PC (the main desktop PC) has more RAM and cores and could carry roughly 12; a cloud box could carry more.

## Sizing rule: lanes per GB of RAM, and per CPU core
Measured: about **1 GB of RAM per working lane all-in** (the agent process is only about 0.3 GB; the rest is the tools it launches: headless Chrome for screenshots, Python, test servers). Plan with headroom:

| Budget item | Allowance |
|---|---|
| Per working lane | **1.5 GB** |
| Operating system + your own apps | 6 GB on a small machine, about 16 GB on a big one |
| Ghidra (one at a time) | 4 GB |
| WSL + DOSBox-X oracle (one at a time) | 2-4 GB |

**RAM limit:** lanes = (total RAM - OS/apps - Ghidra - WSL/oracle) / 1.5.
**CPU limit:** about 1 build/test lane per physical core (they run headless Chrome), or about 2 decode lanes per core (they mostly wait on the model).
**Take the smaller of the two**, then apply the work-shape and Foreman limits below; the usage budget usually binds first on big machines.

| Machine | RAM limit | CPU limit (example) | Recommended |
|---|---|---|---|
| 16 GB handheld, 8 cores (16 GB handheld PC) | (16-6-4-2)/1.5 = about 3-4 heavy lanes; about 6 when lanes are mostly decode | 8 build or 16 decode | **about 6** (cap set after a 12-lane overload) |
| 128 GB desktop, 16+ cores | (128-16-4-6)/1.5 = about 65 | 16 build or 32 decode | **12-16**, with 2 Foremen or sub-foremen; going higher buys little because of the work shape, the Foreman span and the usage budget |

GPUs do not add lanes: the models run in the cloud, and the local tools are CPU-bound. A big GPU is useful only for local helper models (draft/review lanes) and art upscaling.

## 2. The usage window (the shared limit)
All Claude lanes draw on the same subscription session window and weekly budget. Twice as many lanes burn the window twice as fast; the work does not get cheaper, only earlier. Star Command's Foreman paused on a usage limit mid-run. More lanes mean hitting the wall sooner, then everyone waits.

## 3. The shape of the work (Amdahl's law)
The decode has a critical path that cannot be parallelised: unpack, then layout, then the one layer, then areas. Phase 1 had 2-3 useful lanes, not 12. The area phase can only use as many lanes as there are independent areas: Star Command had 7 modules, Pool of Radiance 6 areas. Splitting an area across lanes makes them collide on shared globals and the same pseudocode file.

## 4. The Foreman's span of control
One Foreman reads every STATUS note, routes every fix request, owns every handoff. Past about 8 lanes it becomes the bottleneck and requests sit unanswered (Star Command memory records one that did). More lanes would need sub-foremen per area group, which adds coordination cost.

## Rule
- Lanes = min(independent areas available right now, machine limit, usage headroom). On a 16 GB handheld: <= 6-8.
- Prefer cheap codex lanes for drafts (light on RAM, separate budget) and spend Claude lanes on finals, verification and build.
- Scale up for genuinely bigger games (e.g. a 30-overlay RPG) on the main PC, with sub-foremen per area group.
