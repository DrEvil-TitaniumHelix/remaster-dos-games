#!/usr/bin/env python3
"""release.py: the repeatable release steps of RELEASE.md for one public tree.

Two subcommands. Both are dry runs unless told otherwise; every command is printed before it runs.

  clean <src> <dest> --version vX.Y.Z[-alpha|-beta|-rc.N] [--exclude PATH ...] [--message TEXT] [--run]
      RELEASE.md (b2), ruling RL-2: copy the files git tracks at <src> HEAD (minus --exclude) into the NEW directory
      <dest>, `git init`, set the public identity repo-locally, make ONE commit and tag the version (annotated).
      Never touches <src>. Without --run it only prints the plan.

  publish <tree> --repo OWNER/NAME --version TAG [--public|--private] [--description TEXT] [--zip PATH ...]
          [--gate CMD ...] [--no-zip] [--existing] [--title TEXT] [--dist DIR] [--push]
      RELEASE.md (c)-(f): (c) gates, (d) tag + CHANGELOG section, (e) GitHub repo, (f) GitHub Release with notes and
      a zip for players without git, plus the "original did this too" label. Without --push nothing is created,
      pushed or written: the GitHub commands are printed only (GitHub Pages: none, ruling RL-3 = B).

Refuses (exit 1) when: the tree is dirty; the personal-data gate (tools/personal_gate.py, with the private patterns)
or any --gate command fails; any commit is not authored AND committed by the public identity; the tree has more than
one commit (RL-2) unless --allow-history; the tag is missing or not on HEAD; CHANGELOG.md has no section for it.
Gates are local and read-only, so they also run in a dry run.

Public identity: DrEvil <ID+DrEvil-TitaniumHelix@users.noreply.github.com>, ID from `gh api user --jq .id`
(set with --identity "Name <email>" to override; RELEASE.md hard rule 1).
"""
import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
IDENTITY = 'DrEvil <58350129+DrEvil-TitaniumHelix@users.noreply.github.com>'
TRAILER = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
LABEL = ('original did this too', 'c5def5', 'The DOS original behaves the same way (not a defect of the remake)')
TAG_RX = re.compile(r'^v\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)(?:\.\d+)?)?$')


def show(cmd, cwd=None):
    where = f'(cd {shlex.quote(cwd)}) ' if cwd else ''
    print('$ ' + where + ' '.join(shlex.quote(c) for c in cmd))


def run(cmd, cwd=None, check=True, capture=False):
    show(cmd, cwd)
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=capture)
    if check and r.returncode:
        if capture:
            sys.stdout.write(r.stdout or '')
            sys.stdout.write(r.stderr or '')
        die(f'command failed (exit {r.returncode})')
    return r


def run_retry(cmd, cwd=None, tries=6, wait=15):
    """run() for GitHub calls that may hit a temporary lock: retry every `wait` s, up to `tries` attempts."""
    for n in range(1, tries + 1):
        r = run(cmd, cwd=cwd, check=False, capture=True)
        sys.stdout.write(r.stdout or '')
        if r.returncode == 0:
            return r
        sys.stdout.write(r.stderr or '')
        if n < tries:
            print(f'   attempt {n}/{tries} failed (exit {r.returncode}); retrying in {wait} s')
            time.sleep(wait)
    die(f'command failed after {tries} attempts')


def git(tree, *args):
    return subprocess.run(['git', '-C', tree, *args], text=True, capture_output=True).stdout.strip()


def die(msg):
    print('REFUSED: ' + msg)
    sys.exit(1)


def split_identity(ident):
    m = re.match(r'^(.+?) <([^>]+)>$', ident)
    if not m:
        die(f'bad identity {ident!r}')
    return m.group(1), m.group(2)


def changelog_section(tree, version):
    p = os.path.join(tree, 'CHANGELOG.md')
    if not os.path.exists(p):
        return None
    text = open(p, encoding='utf-8').read()
    m = re.search(r'^## \[?' + re.escape(version) + r'\]?.*?$(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(0).strip() if m else None


# ---------------------------------------------------------------- clean (RL-2: one clean commit in a new directory)
def cmd_clean(a):
    src, dest = os.path.abspath(a.src), os.path.abspath(a.dest)
    if not TAG_RX.match(a.version):
        die(f'version {a.version} is not vX.Y.Z[-alpha|-beta|-rc.N]')
    if git(src, 'status', '--porcelain'):
        die(f'{src} has uncommitted changes')
    if os.path.exists(dest) and os.listdir(dest):
        die(f'{dest} exists and is not empty (never overwrite; remove it by hand if you mean to rebuild)')
    files = [f for f in git(src, 'ls-files', '-z').split('\0') if f]
    ex = [e.rstrip('/') for e in a.exclude]
    keep = [f for f in files if not any(f == e or f.startswith(e + '/') for e in ex)]
    name, email = split_identity(a.identity)
    msg = a.message or f'{os.path.basename(dest)} {a.version}: initial public release'
    print(f'clean: {src} @ {git(src, "rev-parse", "--short", "HEAD")} -> {dest}: {len(keep)} of {len(files)} files '
          f'(excluded: {", ".join(ex) or "none"}), one commit by {a.identity}, tag {a.version}')
    plan = [['git', 'init', '-q', '-b', 'main'], ['git', 'config', 'user.name', name],
            ['git', 'config', 'user.email', email], ['git', 'config', 'core.autocrlf', 'false'], ['git', 'add', '-A'],
            ['git', 'commit', '-q', '-m', msg + '\n\n' + TRAILER],
            ['git', 'tag', '-a', a.version, '-m', f'{os.path.basename(dest)} {a.version}']]
    if not a.run:
        print(f'$ copy {len(keep)} files from {src} HEAD to {dest}')
        for c in plan:
            show(c, dest)
        print('dry run: nothing written (add --run)')
        return 0
    os.makedirs(dest, exist_ok=True)
    print(f'$ copy {len(keep)} files from {src} HEAD to {dest}')
    for f in keep:
        out = os.path.join(dest, f)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        blob = subprocess.run(['git', '-C', src, 'show', f'HEAD:{f}'], capture_output=True, check=True).stdout
        if f.lower().endswith(('.cmd', '.bat')):   # Windows launchers need CRLF in the work tree
            blob = blob.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        open(out, 'wb').write(blob)
    for c in plan:
        run(c, cwd=dest)
    print(f'clean: {dest} = 1 commit {git(dest, "rev-parse", "--short", "HEAD")}, tag {a.version}')
    return 0


# ---------------------------------------------------------------- publish (RELEASE.md c-f)
def cmd_publish(a):
    tree = os.path.abspath(a.tree)
    slug = a.repo.split('/')[-1]
    name, email = split_identity(a.identity)
    print(f'publish: {tree} -> github.com/{a.repo} ({"public" if not a.private else "private"}), {a.version}, '
          f'{"PUSH" if a.push else "dry run"}')
    # (c) gates: clean tree, identity, history, personal data, the repo's own gates
    if git(tree, 'status', '--porcelain'):
        die('tree has uncommitted changes')
    authors = set(git(tree, 'log', '--format=%an <%ae>|%cn <%ce>').splitlines())
    bad = [x for x in authors if any(p != a.identity for p in x.split('|'))]
    if bad:
        die('commits not authored/committed by the public identity: ' + '; '.join(sorted(bad)))
    n = int(git(tree, 'rev-list', '--count', 'HEAD') or 0)
    if n != 1 and not a.allow_history:
        die(f'{n} commits; RL-2 publishes one clean commit (use the clean subcommand, or --allow-history)')
    run([sys.executable, '-I', os.path.join(HERE, 'personal_gate.py'), tree])
    for g in a.gate:
        run(shlex.split(g), cwd=tree)
    print('gates: PASS')
    # (d) version tag + CHANGELOG
    if not TAG_RX.match(a.version):
        die(f'version {a.version} is not vX.Y.Z[-alpha|-beta|-rc.N]')
    if git(tree, 'rev-parse', '-q', '--verify', f'refs/tags/{a.version}^{{commit}}') != git(tree, 'rev-parse', 'HEAD'):
        die(f'tag {a.version} missing or not on HEAD (the clean subcommand creates it)')
    notes = changelog_section(tree, a.version)
    if not notes:
        die(f'CHANGELOG.md has no "## {a.version}" section')
    dist = os.path.abspath(a.dist)
    notes_file = os.path.join(dist, f'{slug}-{a.version}-notes.md')
    zip_file = os.path.join(dist, f'{slug}-{a.version}.zip')
    prerelease = ['--prerelease'] if '-' in a.version else []
    # (e) repository, (f) release + zip + label; nothing below runs without --push
    if a.existing:
        # the GitHub repo already exists (private, older history): replace its history with the clean commit, then
        # change visibility; both only with the owner's explicit approval (RELEASE.md, "This method repo")
        repo_steps = [
            ['git', 'remote', 'add', 'origin', f'https://github.com/{a.repo}.git'],
            ['git', 'push', '--force', 'origin', 'main'],
            ['gh', 'repo', 'edit', a.repo, '--visibility', 'private' if a.private else 'public',
             '--accept-visibility-change-consequences'] + (['--description', a.description] if a.description else []),
        ]
    else:
        repo_steps = [
            ['gh', 'repo', 'create', a.repo, '--private' if a.private else '--public', '--source', '.', '--remote',
             'origin', '--push'] + (['--description', a.description] if a.description else []),
        ]
    steps = repo_steps + [
        ['git', 'push', 'origin', f'refs/tags/{a.version}'],
        ['gh', 'label', 'create', LABEL[0], '--color', LABEL[1], '--description', LABEL[2], '--repo', a.repo,
         '--force'],
        ['gh', 'release', 'create', a.version] + ([] if a.no_zip else [zip_file]) + [
            '--repo', a.repo, '--verify-tag', '--title', a.title or f'{slug} {a.version}', '--notes-file',
            notes_file] + prerelease,
    ]
    print(f'$ write {notes_file} (CHANGELOG section {a.version}, {len(notes)} chars)')
    if not a.no_zip:
        print(f'$ zip {zip_file} <- {slug}/ + {", ".join(a.zip)} at {a.version}')
    for c in steps:
        show(c, tree)
    if not a.push:
        print('dry run: nothing created, pushed or written (add --push only after the owner said "send it")')
        return 0
    os.makedirs(dist, exist_ok=True)
    open(notes_file, 'w', encoding='utf-8', newline='\n').write(notes + '\n')
    files = [f for f in git(tree, 'ls-files', '-z').split('\0') if f]
    with (open(os.devnull, 'w') if a.no_zip else zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)) as z:
        for f in ([] if a.no_zip else files):
            in_zip = any(f == p.rstrip('/') or f.startswith(p.rstrip('/') + '/') for p in a.zip)
            if in_zip or ('/' not in f and f.lower().endswith(('.cmd', '.bat'))):   # + root launchers
                data = subprocess.run(['git', '-C', tree, 'show', f'{a.version}:{f}'], capture_output=True,
                                      check=True).stdout
                if f.lower().endswith(('.cmd', '.bat')):   # Windows launchers need CRLF
                    data = data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
                z.writestr(f'{slug}/{f}', data)
    for i, c in enumerate(steps):
        if a.existing and i >= len(repo_steps):
            # right after a visibility change GitHub answers 'HTTP 403: Repository has been locked' for a short while
            # (seen 2026-10-18 on the label step; a retry ~30 s later succeeded): wait and retry
            run_retry(c, cwd=tree)
        else:
            run(c, cwd=tree)
    print(f'published: https://github.com/{a.repo} release {a.version}')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('clean')
    c.add_argument('src')
    c.add_argument('dest')
    c.add_argument('--version', required=True)
    c.add_argument('--exclude', action='append', default=[])
    c.add_argument('--message')
    c.add_argument('--identity', default=IDENTITY)
    c.add_argument('--run', action='store_true')
    p = sub.add_parser('publish')
    p.add_argument('tree')
    p.add_argument('--repo', required=True)
    p.add_argument('--version', required=True)
    p.add_argument('--private', action='store_true')
    p.add_argument('--public', action='store_true')
    p.add_argument('--description')
    p.add_argument('--title', help='release title (default: <name> <version>)')
    p.add_argument('--zip', action='append', default=[])
    p.add_argument('--gate', action='append', default=[])
    p.add_argument('--no-zip', action='store_true', help='release without a player zip (the method repo)')
    p.add_argument('--existing', action='store_true', help='the GitHub repo exists: force-push the clean commit, then set visibility')
    p.add_argument('--dist', default=os.path.join(os.path.dirname(os.path.dirname(HERE)), 'release-dist'))
    p.add_argument('--identity', default=IDENTITY)
    p.add_argument('--allow-history', action='store_true')
    p.add_argument('--push', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'publish' and not a.zip:
        a.zip = ['game', 'tools/serve.py', 'README.md', 'CHANGELOG.md', 'LICENSE', 'LICENSE-MIT', 'LICENSE-DOCS']
    return cmd_clean(a) if a.cmd == 'clean' else cmd_publish(a)


if __name__ == '__main__':
    sys.exit(main())
