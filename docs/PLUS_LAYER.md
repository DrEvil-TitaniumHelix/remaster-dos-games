# The Plus layer — standard quality-of-life package for every remaster

Standard since 2026-10-19. First implementation: **Gold Box Plus** on the Pool of Radiance remake (built in one day
under the Foreman method; plan `GOLD_BOX_PLUS.md`, contract `docs/PLUS_HOOKS.md`, code `game/plus/`, harness
`game/test/plus/`, rows `acceptance/plus/` in that repo). Second: Star Command (trial of what is shared). Later:
Darklands. Model: Darklands+ (bouchacha, MIT), whose F12 page, quest log, battle log, hooks and mod folders this
follows; Gold Box Companion (closed freeware) for the feature list; FRUA / Dungeon Craft (GPL, design only) for
scenario tools.

## 1. Three layers (the rule)
```
engine   the faithful reproduction or rewrite: untouched behaviour, pixel-exact against the oracle; it only EMITS
         events (one-line call sites) and REGISTERS click regions where it draws
hooks    one file: event bus (never throws into the engine), read-only state access, region registry,
         master switch, two engine-side slots (safe point for saves, asset resolver for mods)
plus     every feature; reads events and state, writes only its own store (IndexedDB / folder `<game>-plus`,
         keyed by save slot); never calls into engine internals
```
Input stays a **key synthesizer**: every mouse, touch or controller action becomes exactly the keys a keyboard
player would press. That is why original mode can be proven unchanged and why the engine never learns about the mouse.

## 2. The hook contract (port this list; rename per game)
Events, each with payload, engine address and timing in `docs/PLUS_HOOKS.md`:
`textPrinted` (every text the game shows, with its source), `areaEntered`, `moved`, `menuDrawn`, `listDrawn`,
`partyDrawn`, `viewDrawn`, `combatStart` / `combatTurn` / `combatCursor` / `combatEnd`, `monsterShown`,
`pictureShown`, `npcTalk`, `treasure`, `flagSet` (every script-visible variable write), `inputStarted` / `inputChanged`
/ `inputEnded` (line prompts), `anyKeyWait`, `saveLoaded`, `gameSaved`; derived events (`journalRef`) are built in
hooks.js from text, never in the engine.
State access (read-only): party, position, clock, script memory / flags, current slot, combat window.
Region registry: every drawn menu word, list row, roster line, map cell, view zone registers
`{ rect, kind, left: keys, right: [options] }`; cleared when its screen stops waiting (stale regions type keys).
Master switch `hooks.enabled = false` = "Play the original game": emit is a no-op, regions empty, every tab inert.

## 3. Standard packages (W numbers from the Pool of Radiance plan)
| package | what | game-independent? |
|---|---|---|
| W1 hooks | the contract above | the shape yes; every emit site is per game |
| W2 shell | panel (F12 / gear / controller Menu / Esc), tabs, settings, store, master switch, Status, Keys, About + CREDITS | yes |
| W3 click | hit regions + modern right-click lists, cursor hints, click-to-travel over the decoded map, combat mouse (left = default action, right = the menu filtered by what the pointer is over), mouse text entry | framework yes; per-screen actions per game |
| W4 notes | automatic diary from events, place + time, per slot, exported with saves; journal entries only from the player's own manual (PDF import) or pasted, shown only once the game referenced them | yes |
| W5 quests | quest table keyed by script flag address with evidence; tab = state machine over `flagSet` + offer texts | table per game |
| W6 pedia | catalogue from the decoded data (monsters, items, spells, places, NPCs) + reveal-on-encounter + search + hand-written how-to pages | framework yes; data sources per game |
| W7 map | automap from decoded map data, visited fog per slot, party marker, click-to-travel | viewer yes; map format per game |
| W8 helpers | crisp font toggle, tooltips, combat log, margins, quick/auto save through the game's own save path, spell/loadout presets | yes, each behind a toggle |
| W9 mods | manifest (`mod.json`), asset overrides by file + record, stack in the store, resolver slot in the data loader, Mods tab, sample recolour skin generated in the browser (ships nothing) | yes |
| W10 profile | `game/profiles/<game>.json` (manifest, data groups, record sizes, areas, quest table, pedia sources), `*-only` markers in the engine, Games selector | yes |
| W11 cheat | state injection: party/crew spec -> records via the game's own creation rules, position, flags, clock; `?scenario=`; dev-only tab | pattern yes; record builders per game |
| W12 scenario | scenario JSON + the writers the decode only read: script assembler (byte-identical round trip), data writer, map editor stub | per game |
| W13 qa | headless routes per tab; isolated committed tree; source fingerprint in every report; the original regression table with Plus mounted | yes |
| W14 release | README section, CREDITS per borrowed feature, CHANGELOG, filtered public clone + gate | yes |

## 4. Gates (every package)
- Player-visible acceptance rows: screenshot route + expected, in `ACCEPTANCE.md` section Plus.
- **Original mode unchanged:** the full existing regression table at 0 px with Plus mounted (Pool of Radiance: 70/70).
- QA runs an isolated copy of the committed tree; a report that saw the source change during the run is void.
- No content shipped: everything shown comes from the player's files or the decode. The public gate scans for it.

## 5. Order and lanes
First slice W1 + W2 + W10 in parallel; W3, W5, W6 as soon as `hooks ready` is posted (W4, W7, W8, W9, W11, W12 need
only W1/W2 and fill free slots). Hooks lane owns the engine files; every other lane files tagged requests to it. Expect
one day with 4 lanes (Opus for hooks, verification and the Foreman; codex for drafts; GLM when it has balance).

## 6. Traps paid for (2026-10-19)
- A stale pointer region (a menu that stopped waiting) types letters into the next screen; clear regions on exit.
- An uncommitted edit to the boot file by one lane stalls every headless run and holds the browser lock: one owner for
  the boot file, and QA runs an isolated committed tree.
- Lanes end their turn with work uncommitted; the Foreman re-prompts "continue, commit by path" (do not merge for them).
- Derived events (journal references) belong in hooks.js, not in the engine: the original has no such opcode.
- Autosave on area entry must skip the entry caused by its own quick load.
