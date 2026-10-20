"""ctx.py LISTING RT [n=4] [before=7] [after=3]: show call contexts of a runtime routine in a module listing."""
import sys,re
lst=open(sys.argv[1]).read().splitlines(); rt=sys.argv[2]
n=int(sys.argv[3]) if len(sys.argv)>3 else 4; b=int(sys.argv[4]) if len(sys.argv)>4 else 7; a=int(sys.argv[5]) if len(sys.argv)>5 else 3
hits=[i for i,l in enumerate(lst) if l.endswith("CALL "+rt)]
step=max(1,len(hits)//n)
for i in hits[::step][:n]:
    print("---- %s (%d uses)"%(rt,len(hits))); print("\n".join(l[7:] for l in lst[max(0,i-b):i+a+1]))
