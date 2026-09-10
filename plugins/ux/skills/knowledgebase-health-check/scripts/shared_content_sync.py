#!/usr/bin/env python3
"""Catch-up check for shared-repo folders that never got a symlink — and for
shared folders whose vault side has since been deleted.

`setup-my-knowledge-base` walks the shared clone's top-level contents and
symlinks each one in — but only once, during that person's own setup. If a
teammate creates a brand-new shared wiki afterward (via `new-project-setup`,
"share this wiki" = yes), that new folder lands in the shared clone but
nobody else's knowledge base ever re-walks the clone to notice it. A `git
pull` on an existing symlink refreshes content inside it; it does nothing for
a folder that has no symlink at all yet. This script re-runs that walk as a
catch-up pass, so a health check catches the gap instead of it going silent.

An un-symlinked shared folder can mean two different things, though: brand
new (nothing else in the vault mentions it yet) or orphaned (a project that
WAS linked in got deleted from the vault without its shared copy being
cleaned up). Those need opposite fixes — link it in, versus offer to clean
it up — so this script tells them apart by checking whether the folder's
name is mentioned anywhere else in the vault's own note text.

Read-only: pulls the shared clone (fast-forward only) but never touches the
knowledge base itself. Creating the missing symlink(s) it reports is a
follow-up step for the person running the check, same as every other finding
in this skill.

Usage:
    python shared_content_sync.py [vault_path] [--json]
"""
import os, sys, json, subprocess

SKIP_DIRS = {'.git', '.obsidian', '.claude', 'node_modules'}


def find_clone_root(vault_root):
    """Resolve the shared clone from an existing symlink into it.

    Looks under 2-Areas/ and 1-Projects/*/ for a symlink (the Research
    Repository link, or a product wiki's Wiki/ link), follows it to the real
    path, then walks up to the nearest ancestor containing .git — that's the
    clone root, wherever it happens to live on this machine.
    """
    candidates = []
    areas = os.path.join(vault_root, '2-Areas')
    if os.path.isdir(areas):
        for name in os.listdir(areas):
            candidates.append(os.path.join(areas, name))
    projects = os.path.join(vault_root, '1-Projects')
    if os.path.isdir(projects):
        for area in os.listdir(projects):
            candidates.append(os.path.join(projects, area, 'Wiki'))

    for path in candidates:
        if os.path.islink(path):
            real = os.path.realpath(path)
            probe = real
            while probe != os.path.dirname(probe):
                if os.path.isdir(os.path.join(probe, '.git')):
                    return probe
                probe = os.path.dirname(probe)
    return None


def git_pull(clone_root):
    try:
        result = subprocess.run(
            ['git', 'pull', '--ff-only'], cwd=clone_root,
            capture_output=True, text=True, timeout=30)
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except Exception as e:
        return False, str(e)


FULLY_SHARED_NAMES = {'Research Repository', 'Brand and Design System'}


def shared_folders(clone_root):
    """Every folder in the clone this vault is meant to link to.

    Mirrors setup-my-knowledge-base Step 4 exactly: each name in
    FULLY_SHARED_NAMES symlinks whole (CLAUDE.md included) to 2-Areas/<name>,
    plus any other top-level folder containing a Wiki/ subfolder, which
    symlinks just its Wiki/ into 1-Projects/<name>/Wiki.
    """
    out = []
    for name in sorted(os.listdir(clone_root)):
        if name in SKIP_DIRS or name.startswith('.'):
            continue
        full = os.path.join(clone_root, name)
        if not os.path.isdir(full):
            continue
        if name in FULLY_SHARED_NAMES:
            out.append({'name': name, 'clone_path': full, 'kind': 'fully-shared'})
        elif os.path.isdir(os.path.join(full, 'Wiki')):
            out.append({'name': name, 'clone_path': os.path.join(full, 'Wiki'), 'kind': 'wiki'})
    return out


def linked_targets(vault_root):
    """Real paths every existing symlink in the vault already resolves to."""
    linked = set()
    for base_name in ('2-Areas', '1-Projects'):
        base = os.path.join(vault_root, base_name)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for d in list(dirs):
                full = os.path.join(root, d)
                if os.path.islink(full):
                    linked.add(os.path.realpath(full))
                    dirs.remove(d)  # don't walk through the symlink itself
    return linked


def mentioned_in_vault(vault_root, name):
    """Whether `name` turns up anywhere in the vault's own note text.

    Distinguishes two reasons a shared folder can be un-symlinked: a brand
    new folder nobody has linked in yet (some note still refers to it — a
    Routing Map row, a MEMORY.md line) versus a project that WAS linked and
    got deleted from the vault, leaving nothing that mentions it at all.
    """
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.md'):
                continue
            try:
                with open(os.path.join(root, fn), 'r', encoding='utf-8', errors='ignore') as fh:
                    if name in fh.read():
                        return True
            except OSError:
                continue
    return False


def check(vault_root):
    clone_root = find_clone_root(vault_root)
    if not clone_root:
        return {'clone_found': False}

    pulled, pull_output = git_pull(clone_root)
    linked = linked_targets(vault_root)
    unlinked = [f for f in shared_folders(clone_root)
                if os.path.realpath(f['clone_path']) not in linked]
    missing = [f for f in unlinked if mentioned_in_vault(vault_root, f['name'])]
    orphaned = [f for f in unlinked if f not in missing]

    return {
        'clone_found': True,
        'clone_root': clone_root,
        'pull_ok': pulled,
        'pull_output': pull_output,
        'missing': missing,
        'orphaned': orphaned,
    }


def report(r):
    if not r['clone_found']:
        return ''
    lines = []
    if not r['pull_ok']:
        lines.append(f"## Shared repo pull failed ({r['clone_root']})")
        lines.append(f"  {r['pull_output']}")
        lines.append("  Couldn't confirm the clone is current — the check below may be stale.")
        lines.append("")
    if r['missing']:
        lines.append(f"## Shared folders with no symlink yet ({len(r['missing'])})")
        for f in r['missing']:
            if f['kind'] == 'fully-shared':
                lines.append(f"  {f['name']} — not linked at 2-Areas/{f['name']}")
            else:
                lines.append(f"  {f['name']} — not linked at 1-Projects/{f['name']}/Wiki")
        lines.append("  Offer to create the missing symlink(s), mirroring setup-my-knowledge-base")
        lines.append("  Step 4 — and add a Routing Map row per Step 6, for each one accepted.")
        lines.append("")
    if r.get('orphaned'):
        lines.append(f"## Orphaned shared folders ({len(r['orphaned'])})")
        for f in r['orphaned']:
            lines.append(f"  {f['name']} — still in the shared clone, but nothing in the vault mentions it anymore")
        lines.append("  Likely a deleted project whose shared copy never got cleaned up. Don't just")
        lines.append("  re-link it in — ask the user first: check Trash for the deleted local folder")
        lines.append("  and restore it (safest), or pull a fresh copy back down, or, only if they're")
        lines.append("  sure, delete it from the shared clone via contribute-to-shared-knowledgebase")
        lines.append("  (opens a PR for someone else to review — never merge it directly).")
        lines.append("")
    return '\n'.join(lines)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    result = check(args[0] if args else '.')
    if '--json' in sys.argv:
        print(json.dumps(result, indent=1))
    elif not result['clone_found']:
        print('No shared-repo clone found — skipping this check.')
    else:
        out = report(result)
        print(out if out else 'Shared repo pulled OK; every shared folder already has a symlink.')
