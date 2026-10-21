# Lane: rt-naming — name every BRUN30 runtime routine Star Command uses

Read FOREMAN.md first (methodology, evidence rule). Work only in `decode/brun30/`.

Inputs: `used_routines.tsv` (140 routines, use counts), `rt_asm.txt` (body disassembly of each), `funcs/*.c` (Ghidra decompile, name RT3x_nn or FUN_1000_xxxx), `summary.tsv`, `brun30_tables.json`, game-side contexts via `python decode/tools/ctx.py decode/listings/SPACE.lst RT3E_42 4 8 3` (Windows python) — run from repo root.

Already proven (do not redo, extend): see `RT_LEDGER.md` table. Conventions: FAC = float accumulator at BRUN DS:0x1A..0x1D (MBF single); [0x1E] end of FAC area; routines calling 0x1F6B set up an overflow frame; 0x99CC = inline (op,type) dispatcher; 0x1EC3 = jump table by one inline byte after the game-side call (RT3F_71/85/95/9D).

Output: (1) append a row per routine to `RT_LEDGER.md` (name, conf H/M/L, evidence: body offsets + one game-side context); (2) update `rt_names.json` (short label per routine; keep the existing format `"RT3F_7B": "FMOV [DI]<-[SI]  ; ..."`); (3) list routines that take extra inline bytes in a new file `inline_args.json` (`{"RT3F_71": 1, ...}`) so qbdis.py can consume them.
Priority order = use count. Mark L when unsure; never guess silently. Expect families: PRINT/LOCATE/COLOR/CLS/SCREEN, INPUT/INKEY$, string ops (concat, MID$, LEN, VAL, STR$, comparisons), FP arithmetic (add, sub, mul, div, compare, int, abs, sqr, sin/cos, rnd), FOR/NEXT support, arrays (DIM/erase/bounds), GOSUB/RETURN/ON..GOTO, BLOAD/BSAVE/OPEN/CLOSE/GET/PUT file, graphics PUT/GET/LINE/PSET/CIRCLE/PAINT, SOUND/PLAY, error trapping (ON ERROR, RESUME), RANDOMIZE/TIMER.
When done: regenerate listings (`wsl.exe -d Ubuntu -- bash -c "cd /mnt/<projects>/StarCommandRE/decode/tools && for m in SPACE STARPORT INSIDE PLBATTLE SPBATTLE STARTUP STARCOMM; do python3 qbdis.py /mnt/<targets>/starcommand/starcoma/$m.EXE --out ../listings/$m.lst; done"`), commit, write a 5-line status to STATUS.md.
