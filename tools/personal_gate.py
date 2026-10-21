#!/usr/bin/env python3
"""Personal-data gate for a tree that is about to be published.

Scans every file git tracks in <tree> (or, with --worktree, every file under it except .git) for personal and
machine details: user paths, network addresses, session / pane ids, Windows host names, phone numbers, street
addresses, e-mail addresses, names of sites games were obtained from, and the owner's private patterns (names,
accounts, machines, persona). Exit 0 = zero hits, 1 = hits (listed), 2 = usage error or private patterns missing.

The owner's own patterns are not in this public file. They live in a private file outside every repo, one
`name<TAB>regex` per line ('#' comments): ~/.config/remaster-dos-games/personal-patterns.txt, or the file named by
env PERSONAL_GATE_PATTERNS. Without it the gate refuses to run unless --generic-only is given.

Allowed: hits listed in <tree>/.personal-gate-allow (one `path:regex` per line, '#' comments) for game text that
happens to match, e.g. a game sentence with the word "ally"; path `*` = any file. Each allow line must say why
in a comment.

Usage: python -I tools/personal_gate.py <tree> [--worktree] [--files-only] [--generic-only]
Tested on: remaster-dos-games, star-command-remake, pool-of-radiance-remake (2026-10-18).
"""
import os
import re
import subprocess
import sys

PATTERNS = [
    ('lan-address', r'\b10\.0\.0\.\d*|\b192\.168\.\d+\.\d+'),
    ('user-path', r'c:\+users\+|c:/users/|/mnt/c/users/'),
    ('session-id', r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'),
    ('pane-id', r'\bw\d+:p\d+\b'),
    ('windows-host', r'\b(?:desktop|laptop)-[a-z0-9]{7}\b'),
    ('phone', r'(?<![\w.:-])\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?![\w.-])'),
    ('street', r'(?-i:\b\d{2,5} [A-Z][a-z]+ (?:Street|Avenue|Boulevard|Road|Drive|Lane)\b)'),
    # where copies of games came from (owner ruling 2026-10-18): never named in a public tree
    ('game-source', r'abandon(?:ia|ware)|myabandon|archive\.org|internet archive|old-games\.(?:com|ru)|dosgamesarchive'
                    r'|classicdosgames|vetusware|winworldpc|gog-games|squakenet|dosgames\.com|playclassic'),
    ('e-mail', r'[\w.+-]+@(?!users\.noreply\.github\.com|anthropic\.com)[\w-]+\.[a-z]{2,}'),
]
PRIVATE = os.environ.get('PERSONAL_GATE_PATTERNS') or os.path.join(
    os.path.expanduser('~'), '.config', 'remaster-dos-games', 'personal-patterns.txt')
SELF = 'tools/personal_gate.py'
RX = []
SKIP_EXT = {'.png', '.jpg', '.gif', '.ico', '.zip', '.wav', '.pdf', '.woff', '.woff2'}


def load_private():
    pats = []
    for line in open(PRIVATE, encoding='utf-8'):
        line = line.rstrip('\r\n')
        if line.strip() and not line.lstrip().startswith('#') and '\t' in line:
            name, rx = line.split('\t', 1)
            pats.append((name.strip(), rx))
    return pats


def files(tree, worktree):
    if not worktree:
        out = subprocess.run(['git', '-C', tree, 'ls-files', '-z'], capture_output=True, check=True).stdout
        return [p for p in out.decode('utf-8').split('\0') if p]
    res = []
    for root, dirs, names in os.walk(tree):
        dirs[:] = [d for d in dirs if d != '.git']
        for n in names:
            res.append(os.path.relpath(os.path.join(root, n), tree).replace('\\', '/'))
    return res


def load_allow(tree):
    allow = []
    p = os.path.join(tree, '.personal-gate-allow')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.split('#', 1)[0].strip()
            if line and ':' in line:
                path, rx = line.split(':', 1)
                allow.append((path, re.compile(rx, re.I)))
    return allow


def scan(tree, worktree=False):
    allow = load_allow(tree)
    if not RX:
        RX.extend((n, re.compile(p, re.I)) for n, p in PATTERNS)
    hits = []
    for rel in files(tree, worktree):
        if os.path.splitext(rel)[1].lower() in SKIP_EXT or rel in ('.personal-gate-allow', SELF):
            continue
        path = os.path.join(tree, rel)
        try:
            data = open(path, 'rb').read()
        except OSError:
            continue
        if b'\0' in data[:8192]:
            continue
        text = data.decode('utf-8', 'replace')
        for no, line in enumerate(text.splitlines(), 1):
            for name, rx in RX:
                for m in rx.finditer(line):
                    if any(ap in (rel, '*') and arx.search(line) for ap, arx in allow):
                        continue
                    hits.append((rel, no, name, m.group(0)))
    return hits


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    if len(args) != 1:
        print(__doc__)
        return 2
    if '--generic-only' not in argv:
        if not os.path.exists(PRIVATE):
            print(f'personal gate: private patterns file missing ({PRIVATE}); refusing (use --generic-only to skip)')
            return 2
        PATTERNS.extend(load_private())
    hits = scan(args[0], '--worktree' in argv)
    files_hit = sorted({h[0] for h in hits})
    if '--files-only' in argv:
        for f in files_hit:
            print(f)
    else:
        for rel, no, name, s in hits:
            print(f'{rel}:{no}: [{name}] {s}')
    print(f'personal gate: {len(hits)} hits in {len(files_hit)} files -> {"PASS" if not hits else "FAIL"}')
    return 0 if not hits else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
