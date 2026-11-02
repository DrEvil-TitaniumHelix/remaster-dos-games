# Branch coverage: verification by play-through from snapshots (method revision 2026-10-30)

**Status: being proven on Secret of the Silver Blades (Gold Box Unified, 2026-10-30). The owner ruled it a core concept of the method the same day; the numbers below are that pilot's and will be replaced by measured ones.**

## 1. The idea in one paragraph
A turn-based DOS game only advances when the player answers a prompt. Once every such prompt is a **Decision as data** and the engine can **snapshot and restore at any decision** (the play API, THE FIRST RULE in METHOD.md), the game is a deterministic step function over its inputs and seeds. Then the number of end-to-end play-throughs needed to test it is **not** the astronomical product of all choices. It is one end-to-end run that plants a snapshot at every branching decision, plus **one short run per branch option**, each starting from its snapshot and playing only to the next checkpoint. A branch run takes seconds to a couple of minutes. The whole catalogue of options for a game is lane-hours.

## 2. The three stages, in this order (the owner, 2026-10-30)
1. **Decode** first. The branch ledger is only as complete as the decoded scripts, and the engine must be faithful before testing it means anything.
2. **Rebuild with the play API inserted.** Every wait-for-input primitive emits a Decision and awaits a Choice; screen and AI are two answerers the game cannot tell apart; snapshot/restore at any decision; state hash per decision; a trace replays to the same hash.
3. **The verification loop** = branch coverage (this document), with a little learning of how battles and engagement work in that game's battle space.

## 3. The reduction
| Level | What | Size (Silver Blades estimate) |
|---|---|---|
| Astronomical | every combination of every choice, played end to end | ~2^450 |
| Exhaustive, finite | every option taken from its snapshot, in every flag state that changes it (the decoded graph names the flag writers) | low thousands |
| First pass | every option taken once | ~1,000 (400-500 branch points) |

The first pass finds most bugs in a few lane-hours. The exhaustive level is the gate. Nobody plays whole-game combinations.

## 4. The ledger
Built from the decoded script graph (every branching event, its options, the flags each sets), committed as ids and numbers only (no game text): `acceptance/<title>/play/BRANCHES.json`. Coverage is reported beside it (`COVERAGE.json`): branches taken / total, quests completed on at least one path, areas fully explored, divergences open.

## 5. A run
Restore the snapshot at branch point B, take option k, play with the model-free executor to the next checkpoint or the next branch point. Every branching decision met on the way snapshots, so forks are free. Budget: 120 s; a slower run is itself a finding (a "slow" divergence). Result: `{branch, option, decisions, wall, divergences, new branch points}`. A **divergence** (an unexpected decision kind, a lost fight, a key wait with no decision, a step the executor cannot play) stops the run and is a bug to root-cause. A fix never restarts anything: the run resumes from its last snapshot and the trace prefix must replay to the same hash.

## 6. No model between clicks
The executor plays plan steps at machine speed through the same API the screen uses (Gold Box pilot: ~290 decisions/s in data mode vs 0.15 decisions/s with a model choosing each decision). A model is called only at a divergence, to amend the local plan or tactics; then the executor resumes. The gate journal is one continuous trace; nothing is played in parallel on it. Branch runs are scheduled as a file queue of `{branch, option}` jobs that any free lane claims.

## 7. The only cheat is the party
To make every decision reachable without losing time to fights, the coverage party is overpowered: 3-4 levels above the guide level for each fight, with the best gear, applied by a debug-only tool that is journalled and asserted absent from the player build. It wins every battle with one simple doctrine: ranged weapons and spells at distance, melee closes as soon as possible, wipe the enemy. **It never cheats past decision making, dialogue or navigation**: every decision, every dialogue, every step is played and journalled, on every branch. No skips, no flag-setting, no teleports past content. Combat correctness at the real guide level is a separate lane (each scripted fight on its own, several seeds).

## 8. The compatibility principle (the owner: "one of the most important things")
**The rebuild must be compatible with this framework.** Any point that cannot be snapshotted, restored or replayed to the same hash is a port bug (hidden state outside the game state) or a misunderstanding of the game architecture (an unaccounted input or clock), never a spot to exempt. The one named exception: the original game's own non-determinism (uninitialised reads, timers), which is made an explicit input and documented. Pilot example: a second restore in one process crashed because a view was bound to the wrong memory; demanding restore-anywhere found a real port bug.

## 9. Where the older methods go
Byte-perfect data and pixel-perfect renderings (and the optional DOSBox oracle) stay as the faithfulness gate: headless runs cannot see a wrong wall or colour. They become a small fixed part of the process. Headless branch coverage is the main verification instrument.

## 10. The deliverable: a skill, not an essay
The remaker should be able to ask the repo, through Claude Code, **"test my game by play-through"** and get a coverage number and a bug list. Building the ledger from the decode, planting snapshots, scheduling branch runs and reporting coverage live inside the skill. The user need not understand the combinatorial reduction. Open for a later revision (after the pilot): building and pruning the decision graph ahead of time.

## 11. Limits
Turn-based games only. A fully open-world or real-time game has no finite decision graph; a virtual clock treated as one more input extends the method to timers (Gold Box already does this) but not to live action.
