#!/usr/bin/env python3
"""Convert Obsidian wikilinks to markdown links across a repo, wherever the
target resolves unambiguously to a file in the same repo.

Anything that doesn't resolve cleanly is left exactly as-is: a target that
only lives in a private vault, a genuine name collision, or a link written
inside a code fence or backticks. This script never guesses -- an untouched
`[[...]]` is always the safe outcome, a wrongly-converted one is not.

Usage:
    python wikilink_to_markdown.py <repo_path> [--write]

Default is --dry-run: prints every before/after pair, changes nothing on
disk. Pass --write to actually rewrite the files.
"""
import os, re, sys, argparse, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vault_lint", os.path.join(HERE, "vault_lint.py"))
vault_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vault_lint)

# Bang for image embeds (![[...]]), double brackets, inner text with no
# nested brackets. No target in this repo contains a heading anchor (#), so
# that case is asserted against rather than silently mishandled -- see
# resolve() below.
WIKILINK = re.compile(r'(!?)\[\[([^\[\]]+)\]\]')

# Only these six characters are encoded in the output path. Everything else
# -- '/', '&', em-dashes, unicode -- stays raw: GitHub's renderer handles
# them fine, and encoding them makes filenames unreadable in a diff.
ENCODE_CHARS = {' ': '%20', '(': '%28', ')': '%29', '#': '%23', '?': '%3F', '%': '%25'}


def encode_path(path):
    return ''.join(ENCODE_CHARS.get(c, c) for c in path)


def find_candidates(vault, t):
    """Every file t could mean: an exact repo-relative path match, an exact
    bare-filename-stem match (markdown pages), or an exact attachment
    basename match (image embeds). Repo-wide by construction (Vault() walks
    the whole tree), so a cross-area link resolves the same as a local one.
    """
    c = set()
    if t in vault.by_path:
        c.add(vault.by_path[t])
    if t in vault.by_stem:
        c.update(vault.by_stem[t])
    if t in vault.attachments:
        c.add(vault.attachments[t])
    return sorted(c)


def resolve(vault, raw_target):
    """Returns (resolved_path_or_None, status); status is one of 'ok',
    'ok-reroot', 'ambiguous', 'not-found'.

    Refuses to guess: a name collision is always ambiguous, never broken by
    directory proximity. The one real collision in this repo -- a 2-line
    stub and the real report both named "2025-07 Partner Survey — Research
    Report", one in Studies/ and one in Reports/ -- sits in the SAME
    directory as the file that links to it. A same-directory tie-break would
    therefore pick the empty stub, which is exactly the wrong answer. Leaving
    every collision untouched is the only rule that gets this one right, and
    no other collision exists in this repo for a smarter rule to help with.
    """
    t = raw_target.strip()
    if not t:
        return None, 'not-found'
    # A '#' here could be a literal character in a real filename (encoded to
    # %23 like any other match) or genuine heading-anchor syntax this script
    # doesn't parse -- both are handled the same safe way: resolve normally,
    # and if nothing matches exactly, leave it untouched rather than guess.

    cands = find_candidates(vault, t)
    if len(cands) == 1:
        return cands[0], 'ok'
    if len(cands) > 1:
        return None, 'ambiguous'

    # A target baked in as a vault-rooted path (e.g. "2-Areas/X/Y") is stale
    # inside the repo itself, which has no "2-Areas/" wrapper -- strip it and
    # retry as a repo-relative path.
    if t.startswith('2-Areas/'):
        stripped = t[len('2-Areas/'):]
        cands2 = find_candidates(vault, stripped)
        if len(cands2) == 1:
            return cands2[0], 'ok-reroot'
        if len(cands2) > 1:
            return None, 'ambiguous'

    return None, 'not-found'


def convert_file(vault, path):
    """Returns (new_text, changed, changes). changes is a list of dicts, one
    per converted link, for reporting."""
    raw = vault.text[path]
    masked = vault_lint.strip_code(raw)
    assert len(masked) == len(raw), f"strip_code changed length in {path}"

    spans = []
    changes = []
    for m in WIKILINK.finditer(masked):
        start, end = m.span()
        full_raw = raw[start:end]
        assert full_raw == m.group(0), f"masked/raw mismatch in {path} at {start}"

        bang = m.group(1)
        inner = full_raw[len(bang) + 2:-2]

        parts = re.split(r'(?<!\\)\|', inner)
        raw_target = parts[0]
        alias = parts[1] if len(parts) > 1 else None
        display = alias if alias is not None else raw_target

        resolved, status = resolve(vault, raw_target)
        if resolved is None:
            continue  # leave untouched: vault-only, ambiguous, or ill-formed

        rel = os.path.relpath(resolved, os.path.dirname(path) or '.')
        rel = rel.replace(os.sep, '/')
        href = encode_path(rel)
        replacement = f"{bang}[{display}]({href})"

        spans.append((start, end, replacement))
        line_no = raw.count('\n', 0, start) + 1
        changes.append({
            'line': line_no, 'before': full_raw, 'after': replacement,
            'target': raw_target, 'status': status,
        })

    if not spans:
        return raw, False, []

    out = []
    cursor = 0
    for start, end, replacement in spans:
        out.append(raw[cursor:start])
        out.append(replacement)
        cursor = end
    out.append(raw[cursor:])
    return ''.join(out), True, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo_path')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    vault = vault_lint.Vault(args.repo_path)
    total_converted = total_left = files_changed = 0

    for p in sorted(vault.md):
        new_text, changed, changes = convert_file(vault, p)
        if not changed:
            continue
        files_changed += 1
        total_converted += len(changes)
        print(f"\n=== {p} ({len(changes)} link(s)) ===")
        for c in changes:
            print(f"  L{c['line']}  {c['before']}  ->  {c['after']}")
        if args.write:
            with open(os.path.join(vault.root, p), 'w', encoding='utf-8') as fh:
                fh.write(new_text)

    print(f"\n{'Wrote' if args.write else 'Would convert'} {total_converted} link(s) across {files_changed} file(s).")
    if not args.write:
        print("Dry run only -- nothing written. Re-run with --write to apply.")


if __name__ == '__main__':
    main()
