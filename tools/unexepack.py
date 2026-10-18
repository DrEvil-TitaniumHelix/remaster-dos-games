"""Unpack a Microsoft EXEPACK-compressed MZ executable (Pool of Radiance START.EXE).

Usage: python unexepack.py IN.EXE OUT.EXE [--report]

Algorithm (verified against the stub code in START.EXE itself, see decode/LAYOUT.md "EXEPACK"):
  EXEPACK header at CS:0000 of the packed image (18 bytes, IP=0012):
    +00 real_IP  +02 real_CS  +04 mem_start(scratch)  +06 exepack_size
    +08 real_SP  +0A real_SS  +0C dest_len (paragraphs)  +0E skip_len  +10 'RB'
  Packed data = load module [0 : CS*16 - (skip_len-1)*16], decompressed BACKWARDS
  into a buffer of dest_len*16 bytes.  Trailing 0xFF padding (<=15 bytes) is skipped.
  Each command (read backwards): cmd byte, length word;
    cmd&0xFE == 0xB0: fill  -> one fill byte, write it `length` times
    cmd&0xFE == 0xB2: copy  -> copy `length` bytes
    cmd&1: last command.
  Packed relocation table follows the "Packed file is corrupt" message
  (stub: MOV SI,012Dh): for seg = 0x0000,0x1000,...,0xF000: count word, count offset words.
"""
import struct, sys


def unpack(raw):
    (sig, cblp, cp, crlc, cparhdr, minalloc, maxalloc, ss, sp, csum, ip, cs, lfarlc, ovno) = \
        struct.unpack_from("<2s13H", raw, 0)
    assert sig in (b"MZ", b"ZM")
    hdr = cparhdr * 16
    size = (cp - 1) * 512 + cblp if cblp else cp * 512
    lm = raw[hdr:size]
    eh = cs * 16
    real_ip, real_cs, mem_start, exe_size, real_sp, real_ss, dest_len, skip_len = \
        struct.unpack_from("<8H", lm, eh)
    if lm[eh + 16:eh + 18] == b"RB":
        hlen = 18
    else:  # older variant without skip_len
        skip_len = 1
        hlen = 16
        assert lm[eh + 14:eh + 16] == b"RB", "no EXEPACK 'RB' signature"
    info = dict(real_ip=real_ip, real_cs=real_cs, real_sp=real_sp, real_ss=real_ss,
                exepack_size=exe_size, dest_len=dest_len, skip_len=skip_len, hdr_len=hlen,
                packed_cs=cs, packed_ip=ip, minalloc=minalloc, maxalloc=maxalloc)
    stub = lm[eh:eh + exe_size]
    msg = b"Packed file is corrupt"
    mi = stub.find(msg)
    assert mi > 0, "stub message not found"
    reloc_off = mi + len(msg)
    info["reloc_table_off_in_stub"] = reloc_off

    # --- backwards decompression
    src_end = cs * 16 - (skip_len - 1) * 16
    buf = bytearray(max(dest_len * 16, src_end))
    buf[:src_end] = lm[:src_end]
    s = src_end - 1
    pad = 0
    while buf[s] == 0xFF and pad < 16:
        s -= 1; pad += 1
    info["ff_padding"] = pad
    d = dest_len * 16 - 1
    ncmd = 0
    while True:
        cmd = buf[s]; s -= 1
        length = buf[s] << 8 | buf[s - 1]; s -= 2
        ncmd += 1
        op = cmd & 0xFE
        if op == 0xB0:
            fill = buf[s]; s -= 1
            for _ in range(length):
                buf[d] = fill; d -= 1
        elif op == 0xB2:
            for _ in range(length):
                buf[d] = buf[s]; d -= 1; s -= 1
        else:
            raise ValueError("bad EXEPACK command %02X at %X" % (cmd, s + 1))
        if cmd & 1:
            break
    info["commands"] = ncmd
    info["final_src"] = s + 1
    info["final_dst"] = d + 1
    image = bytes(buf[:dest_len * 16])

    # --- relocation table
    relocs = []
    p = reloc_off
    for segi in range(16):
        n = struct.unpack_from("<H", stub, p)[0]; p += 2
        for _ in range(n):
            off = struct.unpack_from("<H", stub, p)[0]; p += 2
            relocs.append((off, segi * 0x1000))
    info["relocs"] = len(relocs)
    info["reloc_table_end_in_stub"] = p
    return image, relocs, info


def build_mz(image, relocs, info):
    nrel = len(relocs)
    hdr_bytes = 0x1C + 4 * nrel
    hdr_paras = (hdr_bytes + 15) // 16
    hdr_paras = max(hdr_paras, 2)
    total = hdr_paras * 16 + len(image)
    cp = (total + 511) // 512
    cblp = total % 512
    # extra memory: keep the packed file's requirement relative to the original image end
    packed_total_paras = info["packed_cs"] + (info["exepack_size"] + 15) // 16
    minalloc = max(0, packed_total_paras + info["minalloc"] - len(image) // 16)
    h = struct.pack("<2s13H", b"MZ", cblp, cp, nrel, hdr_paras, minalloc, info["maxalloc"],
                    info["real_ss"], info["real_sp"], 0, info["real_ip"], info["real_cs"], 0x1C, 0)
    h += b"".join(struct.pack("<HH", o, s) for o, s in relocs)
    h = h.ljust(hdr_paras * 16, b"\0")
    return h + image


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    raw = open(a[0], "rb").read()
    image, relocs, info = unpack(raw)
    out = build_mz(image, relocs, info)
    open(a[1], "wb").write(out)
    for k, v in info.items():
        print("%-24s %s" % (k, hex(v) if isinstance(v, int) else v))
    print("%-24s %d bytes (image %d)" % ("output", len(out), len(image)))


if __name__ == "__main__":
    main()
