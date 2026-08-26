#!/usr/bin/env python3
"""Vault-wide link lint for an Obsidian vault.

Reports orphans, broken links, and the specific failure modes that let a vault
silently accumulate disconnected notes. Read-only: never edits anything.

Usage:
    python vault_lint.py [vault_path] [--json] [--quiet]

Every check here exists because it caught something real. The comments say what.
"""
import os, re, sys, json, collections
from urllib.parse import unquote

SKIP_DIRS = {'.obsidian', '.git', '.trash', '.smart-env', 'node_modules',
             '.tmp.driveupload', '.tmp.drivedownload', '.claude'}
# Generic filenames that are agent config or per-folder indexes. They appear in
# prose constantly ("update my CLAUDE.md") and are never citation targets, so
# linking them would create noise hubs and false positives.
GENERIC_STEMS = {'CLAUDE', 'MEMORY', 'index', 'README'}

# Code must be stripped before counting links: a [[link]] inside a fence or
# backticks is an illustration, not a link, and Obsidian does not render it.
# Counting them inflates connectivity and hides real orphans.
CODE_PATTERNS = [re.compile(r'^```.*?^```', re.S | re.M), re.compile(r'`[^`\n]*`')]
WIKI = re.compile(r'\[\[([^\]|#]+)')
MD_LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
ANY_LINK = re.compile(r'\[\[[^\]|#]+|\[[^\]]*\]\([^)]+\)')
SOURCES_LINE = re.compile(r'^\*\*Sources?\*\*:(.*)$', re.M)
INLINE_SOURCE = re.compile(r'\((?:source|Source)s?:\s*([^)]*)\)')
FM_BLOCK = re.compile(r'^---\n(.*?)\n---', re.S)
ALREADY_LINKED = re.compile(r'\[\[[^\]]*\]\]|\[[^\]]*\]\([^)]*\)')

# A "## Sources ingested" list is the one place a wiki deliberately
# inventories its own provenance — and neither pattern above can see it,
# because it is not a **Sources**: line and not a (source: ...) span.
# Four plain-filename citations in the Cashback Card index survived every
# earlier pass for exactly this reason. Capture the bullets under any
# heading whose text begins with "Source"/"Sources".
SOURCES_SECTION = re.compile(
    r'^\#{1,6}[ \t]*Sources?\b[^\n]*\n(.*?)(?=^\#{1,6}[ \t]|\Z)', re.M | re.S)
SOURCES_BULLET = re.compile(r'^[ \t]*[-*+][ \t]+(.*)$', re.M)
FILENAME = re.compile(r'([A-Za-z0-9][^\n\[\]()|*,;`]{2,90}?\.(?:md|pdf|pptx|xlsx|docx|csv|vtt|png|jpg|jpeg|svg|json|mp4|txt|html))')


def strip_code(text):
    for pat in CODE_PATTERNS:
        text = pat.sub(lambda m: ' ' * len(m.group(0)), text)
    return text


class Vault:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.md, self.other = [], []
        for base, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                rel = os.path.relpath(os.path.join(base, f), self.root)
                (self.md if f.endswith('.md') else self.other).append(rel)
        self.by_stem = collections.defaultdict(list)
        for p in self.md:
            self.by_stem[os.path.splitext(os.path.basename(p))[0]].append(p)
        self.attachments = {os.path.basename(p): p for p in self.other}
        self.by_path = {os.path.splitext(p)[0]: p for p in self.md}
        self.text = {}
        for p in self.md:
            with open(os.path.join(self.root, p), encoding='utf-8', errors='replace') as fh:
                self.text[p] = fh.read()

    def resolve(self, target, src):
        # A table cell escapes an alias pipe ([[Note\|Alias]]), so the captured
        # target arrives with a trailing backslash.
        t = target.strip().rstrip('\\').strip()
        if not t:
            return None
        if t in self.by_stem:
            return self.by_stem[t][0]
        if t in self.attachments:
            return self.attachments[t]
        if t in self.by_path:
            return self.by_path[t]
        if t.startswith(('./', '../')):
            rel = os.path.normpath(os.path.join(os.path.dirname(src), t))
            if rel in self.by_path:
                return self.by_path[rel]
        for k, v in self.by_path.items():
            if k.endswith('/' + t):
                return v
        return None

    def link_targets(self, body):
        out = [m.group(1) for m in WIKI.finditer(body)]
        for m in MD_LINK.finditer(body):
            url = m.group(1)
            # data: URIs are embedded base64 images, not links. One of these
            # produced a 600KB "broken link" report before it was filtered.
            if url.startswith(('http', 'mailto', '#', 'data:', 'obsidian:', 'tel:')):
                continue
            out.append(os.path.splitext(unquote(url))[0])
        return [t for t in out if len(t) <= 200 and '\n' not in t]


def lint(vault):
    out_links = collections.defaultdict(set)
    in_links = collections.defaultdict(set)
    broken = collections.defaultdict(list)
    backtick_only = []
    plain_citations = collections.defaultdict(list)
    fm_dead = collections.defaultdict(list)

    for p in vault.md:
        raw = vault.text[p]
        body = strip_code(raw)
        fence_only = CODE_PATTERNS[0].sub(lambda m: ' ' * len(m.group(0)), raw)

        for t in vault.link_targets(body):
            r = vault.resolve(t, p)
            if r and r != p:
                out_links[p].add(r)
                in_links[r].add(p)
            elif not r:
                broken[t.strip().rstrip('\\')].append(p)

        # A file whose only links (wiki- or markdown-style) sit inside backticks
        # looks connected when you read it but is an orphan to the graph. The
        # CBC wiki changelog had 33 such references and zero real links.
        if not ANY_LINK.search(body) and ANY_LINK.search(raw):
            backtick_only.append(p)

        # Citations written as bare filenames. Two constraints keep this honest:
        # restrict to genuine citation contexts, because matching filenames
        # anywhere in prose flags things like "a published DESIGN.md" which is a
        # common noun; and blank out links that already exist, or a correctly
        # linked [[report.pdf]] gets reported as plain text.
        #
        # Uses fence_only (strips ``` blocks but keeps single backticks), not
        # the fully-stripped `body` used above for the link graph. A Sources
        # line wrapping a filename in single backticks (`` `export.png` ``) is
        # a citation choosing a display style, not an illustrative code
        # example — the CBC and Brand & Design System wikis both write real
        # citations this way, and the fully-stripped body made every one of
        # them invisible to this check.
        linkless = ALREADY_LINKED.sub(lambda m: ' ' * len(m.group(0)), fence_only)
        cites = (list(SOURCES_LINE.finditer(linkless))
                 + list(INLINE_SOURCE.finditer(linkless)))
        for sec in SOURCES_SECTION.finditer(linkless):
            cites += list(SOURCES_BULLET.finditer(sec.group(1)))
        for m in cites:
            for fm in FILENAME.finditer(m.group(1)):
                name = fm.group(1).strip().lstrip('-–— ').strip()
                stem = os.path.splitext(name)[0]
                if stem in GENERIC_STEMS:
                    continue
                if (name.endswith('.md') and stem in vault.by_stem
                        and vault.by_stem[stem][0] != p):
                    plain_citations[name].append(p)
                elif not name.endswith('.md') and name in vault.attachments:
                    plain_citations[name].append(p)

        # Frontmatter links that resolve to nothing. Catches an unconfigured
        # Obsidian Web Clipper, whose default author template wraps every
        # article author in [[ ]] — authors never have notes, so each clipping
        # arrives with a permanent dead link. Checks both link styles, same as
        # the body-level graph above.
        fmb = FM_BLOCK.match(raw)
        if fmb:
            for t in vault.link_targets(fmb.group(1)):
                if not vault.resolve(t, p):
                    fm_dead[t.strip().rstrip('\\')].append(p)

    orphans = [p for p in vault.md if not out_links.get(p) and not in_links.get(p)]

    # Two notes whose names differ only by case collide on a case-insensitive
    # filesystem, so a short wikilink can resolve to the wrong one.
    case_clashes = []
    lowered = collections.defaultdict(list)
    for stem, paths in vault.by_stem.items():
        lowered[stem.lower()].extend(paths)
    for low, paths in lowered.items():
        if len({os.path.splitext(os.path.basename(p))[0] for p in paths}) > 1:
            case_clashes.append(sorted(paths))

    root_files = [p for p in vault.md if os.sep not in p and p != 'CLAUDE.md']

    return {
        'counts': {
            'notes': len(vault.md),
            'edges': sum(len(v) for v in out_links.values()),
            'orphans': len(orphans),
            'no_inbound': len([p for p in vault.md if not in_links.get(p) and out_links.get(p)]),
            'no_outbound': len([p for p in vault.md if in_links.get(p) and not out_links.get(p)]),
        },
        'orphans': sorted(orphans),
        'broken_links': {k: sorted(v) for k, v in sorted(broken.items(), key=lambda x: -len(x[1]))},
        'plain_text_citations': {k: sorted(v) for k, v in sorted(plain_citations.items(), key=lambda x: -len(x[1]))},
        'frontmatter_dead_links': {k: sorted(v) for k, v in sorted(fm_dead.items(), key=lambda x: -len(x[1]))},
        'backtick_only_references': sorted(backtick_only),
        'case_collisions': case_clashes,
        'vault_root_files': sorted(root_files),
    }


def report(r, quiet=False):
    c = r['counts']
    lines = [f"notes {c['notes']}  edges {c['edges']}  orphans {c['orphans']}"
             f"  no-inbound {c['no_inbound']}  no-outbound {c['no_outbound']}", ""]

    if r['broken_links']:
        lines.append(f"## Broken links ({sum(len(v) for v in r['broken_links'].values())} instances, {len(r['broken_links'])} unique)")
        for t, where in r['broken_links'].items():
            lines.append(f"  {t} — {len(where)}x, e.g. {where[0]}")
        lines.append("")
    if r['plain_text_citations']:
        lines.append(f"## Citations written as plain text ({len(r['plain_text_citations'])} targets)")
        for t, where in r['plain_text_citations'].items():
            lines.append(f"  {t} — cited by {len(where)} notes, e.g. {where[0]}")
        lines.append("")
    if r['frontmatter_dead_links']:
        lines.append(f"## Frontmatter links resolving to nothing ({len(r['frontmatter_dead_links'])})")
        for t, where in r['frontmatter_dead_links'].items():
            lines.append(f"  {t} — {len(where)}x, e.g. {where[0]}")
        lines.append("")
    if r['backtick_only_references']:
        lines.append(f"## Notes whose only links are inside backticks ({len(r['backtick_only_references'])})")
        for p in r['backtick_only_references']:
            lines.append(f"  {p}")
        lines.append("")
    if r['case_collisions']:
        lines.append(f"## Filenames differing only by case ({len(r['case_collisions'])})")
        for grp in r['case_collisions']:
            lines.append("  " + "  |  ".join(grp))
        lines.append("")
    if r['vault_root_files']:
        lines.append(f"## Files in the knowledge base root ({len(r['vault_root_files'])})")
        for p in r['vault_root_files']:
            lines.append(f"  {p}")
        lines.append("")
    if not quiet and r['orphans']:
        lines.append(f"## Orphans — no links in or out ({len(r['orphans'])})")
        for p in r['orphans']:
            lines.append(f"  {p}")
        lines.append("")
    return '\n'.join(lines)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    vault = Vault(args[0] if args else '.')
    result = lint(vault)
    if '--json' in sys.argv:
        print(json.dumps(result, indent=1))
    else:
        print(report(result, quiet='--quiet' in sys.argv))
