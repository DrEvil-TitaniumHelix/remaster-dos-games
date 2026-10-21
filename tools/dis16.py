"""dis16.py FILE.EXE OFF LEN [--base SEG] : capstone 16-bit disassembly of an MZ load-module range (Linux/WSL)."""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mz import load
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
f,off,ln=sys.argv[1],int(sys.argv[2],16),int(sys.argv[3],16)
lm=load(f)["lm"]
md=Cs(CS_ARCH_X86,CS_MODE_16); md.skipdata=True
for i in md.disasm(lm[off:off+ln],off):
    print("%05X  %-18s %s %s"%(i.address,i.bytes.hex(" "),i.mnemonic,i.op_str))
