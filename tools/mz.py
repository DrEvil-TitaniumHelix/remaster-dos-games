"""MZ load-module helpers for the Star Command decode."""
import struct,sys
def load(path):
    f=open(path,"rb").read()
    e_cblp,e_cp,e_crlc,e_cparhdr,_,_,e_ss,e_sp,_,e_ip,e_cs,e_lfarlc=struct.unpack_from("<12H",f,2)
    hdr=e_cparhdr*16; size=(e_cp-1)*512+e_cblp if e_cblp else e_cp*512
    rel=[struct.unpack_from("<HH",f,e_lfarlc+4*i) for i in range(e_crlc)]
    return dict(raw=f,lm=f[hdr:size],cs=e_cs,ip=e_ip,ss=e_ss,sp=e_sp,relocs=rel,hdr=hdr)
def hexdump(b,base=0,n=None):
    n=n or len(b)
    for off in range(0,n,16):
        row=b[off:off+16]; print("%05X "%(base+off)+row.hex(" ").ljust(48)+"  "+"".join(chr(c) if 32<=c<127 else "." for c in row))
