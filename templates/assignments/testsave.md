# testsave — a ready-to-play save with a fully developed crew (the owner 2026-10-16, relayed by the coordinator)

the owner: "place a fully developed crew in a save game so that I can just start up into the game without having to create the crew every time." Owner: lane `testsave` (Opus). No Fable. Do not touch files owned by build-engine2's v1.1/v1.2 lanes except where listed; write a `<file> request:` note in STATUS.md if you must.

## Deliverable
1. **`game/assets/saves/veteran/CHARINFO.BAS` + `CHARNAME`** = a genuine game save (original BSAVE layout, engine/state.js toBytes) in which:
   - 8 crew members, one per role the game uses (pilot, co-pilot/navigator, comms, engineer, medic, marines/espers as the class table allows), real names, **high rank, max HP, high skills** (as high as the game's own caps and training rules allow; cite the cap from the decode), healthy, rested.
   - Good personal equipment for each: best weapon class each can use, armor, ammo/reloads full, equipment items useful in INSIDE (cite record formats from decode/data + CROSSREF).
   - A capable ship: the best hull the Starport sells, christened, full fuel, weapons/defences fitted, no damage; healthy credits (e.g. 50,000) for testing purchases.
   - Docked at a Starport main menu with no transaction in progress, an active first mission if the game's flow allows it.
   - Every value set from the decode (assets/gmap.json, CROSSREF.md, STARPORT/SPACE pseudocode). Write `game/assets/saves/veteran/README.md` listing each field changed with its G!() index and source. Nothing the game would reject or later "correct" (check the validation paths the modules run on load).
   Build it with a small script `tools/make_veteran_save.mjs` (node, reuses engine/state.js + data.js) so it can be regenerated.
2. **Loading it:** `?save=veteran` on the URL copies that save into the game's storage (engine/files.js write) before boot ONLY when no player save exists yet, or always when `&force=1`. Then the normal start menu's continue option goes straight in with that crew. Add the option to the Esc overlay Settings page later only if v1.2's settings page exists (note for build-engine2, don't edit overlay.js yourself).
3. **Launcher:** `Play Star Command (Veteran Crew).cmd` in the repo root (copy of the existing launcher with `?save=veteran&force=1`), and a Desktop shortcut **on the real desktop `<Desktop>\`** named `Star Command - Veteran Crew.lnk` pointing at it (same icon/working dir as the existing shortcut).
4. **Verify by playing it headlessly:** boot with the save, take screenshots of the Starport main menu, A-Personnel crew list, I-Inspect ship, one SPACE screen after L-Leave, and one PLBATTLE command phase (or the dev jump with this save) into `acceptance/veteran/`; confirm nothing errors and values display as intended. Node tests still pass.

## Done means
Commit `testsave: veteran crew save + launcher`, STATUS block `testsave DONE` listing the crew (name, role, rank, HP, key skills, weapon), the ship, credits, and how to start it.
