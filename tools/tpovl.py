"""Turbo Pascal (FBOV) overlay layout for Pool of Radiance.

Usage: python tpovl.py START.unpacked.exe GAME.OVR [--json out.json] [--extract DIR]

Overlay stub segment (one per overlaid unit, in the resident image; layout read from the bytes,
see decode/LAYOUT.md for evidence):
  +00 CD 3F        INT 3Fh (overlay manager trap)
  +02 word         ReturnAddr (runtime, 0 on disk)
  +04 dword        FileOfs   absolute offset of the unit's code in GAME.OVR
  +08 word         CodeSize
  +0A word         FixupSize (bytes; 2 bytes per fixup = word offset into the code)
  +0C word         EntryPts  (count)
  +0E word         CodeListNext (previous stub segment, image-relative; 0 = end)
  +10..+1F         runtime fields (LoadSeg, Reprieved, LoadListNext, ...) 0 on disk
  +20 + 5*i        entry i: CD 3F <word offset into unit code> 00
GAME.OVR: 'FBOV' + dword (file size - 8), then per unit: code[CodeSize] + fixups[FixupSize].
Each fixup word = offset in unit code of a 16-bit segment value, image-relative
(same convention as MZ relocations: runtime adds PrefixSeg+10h).
"""
import json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mz


def parse(exe, ovr):
    m = mz.load(exe)
    lm = m["lm"]
    o = open(ovr, "rb").read()
    assert o[:4] == b"FBOV"
    ovr_len = struct.unpack_from("<I", o, 4)[0]
    stubs = []
    seg = 0
    # stubs are paragraph aligned; scan for valid headers
    for p in range(0, len(lm) - 0x20, 16):
        if lm[p:p + 2] != b"\xCD\x3F" or lm[p + 2:p + 4] != b"\0\0":
            continue
        fofs, csz, fsz, nent, nxt = struct.unpack_from("<IHHHH", lm, p + 4)
        if not (8 <= fofs < len(o) and nent and fofs + csz + fsz <= len(o)):
            continue
        ents = []
        for i in range(nent):
            q = p + 0x20 + 5 * i
            if lm[q:q + 2] != b"\xCD\x3F":
                break
            ents.append(struct.unpack_from("<H", lm, q + 2)[0])
        if len(ents) != nent:
            continue
        code = o[fofs:fofs + csz]
        fix = [struct.unpack_from("<H", o, fofs + csz + 2 * i)[0] for i in range(fsz // 2)]
        fixsegs = sorted(set(struct.unpack_from("<H", code, f)[0] for f in fix))
        stubs.append(dict(stub_seg=p // 16, file_ofs=fofs, code_size=csz, fixup_size=fsz,
                          n_fixups=len(fix), entries=ents, code_list_next=nxt,
                          stub_size=0x20 + 5 * nent, fixups=fix, fixup_target_segs=fixsegs))
    # resident segments: every segment value named by an MZ relocation or an overlay fixup
    rel_targets = sorted(set(struct.unpack_from("<H", lm, s * 16 + off)[0] for off, s in m["relocs"]))
    return m, o, ovr_len, stubs, rel_targets


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    m, o, ovr_len, stubs, rel_targets = parse(a[0], a[1])
    stub_segs = {s["stub_seg"] for s in stubs}
    print("FBOV payload length %#x (file %#x)" % (ovr_len, len(o)))
    print("overlay units: %d, entries: %d, code bytes: %#x" % (
        len(stubs), sum(len(s["entries"]) for s in stubs), sum(s["code_size"] for s in stubs)))
    end = 8
    for i, s in enumerate(stubs):
        gap = s["file_ofs"] - end
        end = s["file_ofs"] + s["code_size"] + s["fixup_size"]
        print("ov%02d stub %04X fofs %06X code %04X fix %3d ent %3d next %04X gap %d tseg %s" % (
            i, s["stub_seg"], s["file_ofs"], s["code_size"], s["n_fixups"], len(s["entries"]),
            s["code_list_next"], gap, " ".join("%04X%s" % (t, "s" if t in stub_segs else "")
                                               for t in s["fixup_target_segs"])))
    print("end of last unit %#x, file %#x" % (end, len(o)))
    print("resident reloc target segs:", " ".join("%04X%s" % (t, "s" if t in stub_segs else "")
                                                    for t in rel_targets))
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        json.dump(dict(ovr_payload_len=ovr_len, units=stubs, reloc_target_segs=rel_targets),
                  open(out, "w"), indent=1)
    if "--extract" in sys.argv:
        d = sys.argv[sys.argv.index("--extract") + 1]
        os.makedirs(d, exist_ok=True)
        for i, s in enumerate(stubs):
            open(os.path.join(d, "ov%02d_%04X.bin" % (i, s["stub_seg"])), "wb").write(
                o[s["file_ofs"]:s["file_ofs"] + s["code_size"]])


if __name__ == "__main__":
    main()
