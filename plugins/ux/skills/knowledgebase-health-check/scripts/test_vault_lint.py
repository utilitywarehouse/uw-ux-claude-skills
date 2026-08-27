#!/usr/bin/env python3
"""Self-test for vault_lint.py. Builds a small synthetic vault covering every
check, plus the false positives that made earlier versions untrustworthy, and
asserts the lint gets each one right.

Run: python test_vault_lint.py
"""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vault_lint", os.path.join(HERE, "vault_lint.py"))
vl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vl)

FILES = {
    # a real plain-text citation, in both citation forms — should be flagged
    "notes/page.md": "**Sources**: Workshop summary.md\n\n(source: Workshop summary.md)\n",
    "notes/Workshop summary.md": "the source\n",
    # already correctly linked — must NOT be flagged as plain text
    "notes/good.md": "**Sources**: [[Workshop summary]]\n",
    # a filename used as a common noun outside any citation context — must NOT flag
    "notes/prose.md": "A published DESIGN.md bridges the gap.\n",
    "notes/DESIGN.md": "design doc\n",
    # frontmatter link to a note that doesn't exist (unconfigured Web Clipper)
    "notes/clip.md": '---\nauthor:\n  - "[[Some Author]]"\n---\nclipped article\n',
    # same, but markdown-style — the frontmatter check must catch both link styles
    "notes/clip-md.md": '---\nauthor: "[Some Other Author](Some%20Other%20Author.md)"\n---\nclipped article\n',
    # wikilinks only inside backticks — connected to a reader, orphan to the graph
    "notes/log.md": "changed `[[Workshop summary]]` today\n",
    # same, but markdown-style — the backtick-only check must catch both link styles
    "notes/log-md.md": "changed `[Workshop summary](Workshop%20summary.md)` today\n",
    # names differing only by case collide on a case-insensitive filesystem
    "notes/About Me.md": "current\n",
    "arch/About me.md": "superseded\n",
    # a stray note in the vault root
    "stray.md": "should not be here\n",
    # a genuinely broken link
    "notes/points-nowhere.md": "see [[No Such Note]]\n",
    # links inside a fence are illustrations, not links — must not count as edges
    # or as broken links
    "notes/spec.md": "```markdown\n- [[placeholder-name]]\n```\n",
    # a data: URI must not be parsed as a link target
    "notes/img.md": "![x](data:image/png;base64,AAAA)\n",
    # a plain-text citation of a non-md source type, backtick-wrapped — should
    # be flagged. Real wiki pages cite screenshots/JSON this way; the check
    # must see through the backticks to catch it.
    "notes/screenshot-cite.md": "**Sources**: `push-notifications-export.png`\n",
    "notes/push-notifications-export.png": "binary\n",
    # a Sources line *inside a fenced code block* (e.g. a template being shown
    # as an example) must still not be flagged — fenced blocks stay stripped
    "notes/fenced-example.md": "Template:\n\n```markdown\n**Sources**: Workshop summary.md\n```\n",
    # a "## Sources ingested" bullet list — a wiki's own provenance inventory.
    # It is neither a **Sources**: line nor a (source: ...) span, so an earlier
    # version of this check was structurally blind to it and four plain-filename
    # citations in the Cashback Card index survived every pass. The negative
    # cases matter as much as the positive: an already-linked entry in the same
    # list must stay unflagged, and a bullet under an unrelated heading must not
    # be read as a citation just because it names a file.
    "notes/wiki-index.md": (
        "# Index\n\n"
        "## Sources ingested\n\n"
        "- Workshop summary.md \u2014 2026-04-21\n"
        "- [[Ingest notes]] \u2014 2026-04-22\n\n"
        "## Meta\n\n"
        "- Ingest notes.md is discussed here as prose, not cited\n"
    ),
    "notes/Ingest notes.md": "another source\n",
    # a Routing Map whose folders exist, don't exist, or were archived
    "CLAUDE.md": (
        "## Routing Map\n\n"
        "| Folder | Use when... |\n"
        "|---|---|\n"
        "| `1-Projects/Live Project/` | still active — must not be flagged |\n"
        "| `1-Projects/Gone Project/` | archived but the row was never removed |\n"
        "| `1-Projects/Never Existed/` | never had a folder at all |\n"
        "| `2-Areas/Some Guide.md` | a machine-specific path **[replace on setup]** |\n"
    ),
    "1-Projects/Live Project/index.md": "still here\n",
    "4-Archives/Old Area/Gone Project/index.md": "moved here\n",
}

failures = []


def check(label, condition, detail=""):
    if condition:
        print(f"  pass  {label}")
    else:
        print(f"  FAIL  {label}  {detail}")
        failures.append(label)


with tempfile.TemporaryDirectory() as root:
    for rel, body in FILES.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)

    r = vl.lint(vl.Vault(root))
    cites = r["plain_text_citations"]
    broken = r["broken_links"]

    check("flags a plain-text citation", "Workshop summary.md" in cites)
    check("flags a plain filename in a Sources-ingested bullet list",
          "notes/wiki-index.md" in cites.get("Workshop summary.md", []))
    check("does not flag a wikilinked entry in a Sources-ingested list",
          "notes/wiki-index.md" not in cites.get("Ingest notes.md", []))
    check("does not read bullets under a non-Sources heading as citations",
          cites.get("Ingest notes.md", []) == [])
    check("flags a plain-text citation of a non-md source type",
          "push-notifications-export.png" in cites, f"got {list(cites)}")
    check("ignores a Sources line inside a fenced code block",
          os.path.join("notes", "fenced-example.md") not in cites.get("Workshop summary.md", []),
          f"got {cites.get('Workshop summary.md')}")
    check("does not flag an already-linked source",
          os.path.join("notes", "good.md") not in cites.get("Workshop summary.md", []))
    check("does not flag a filename used as a common noun", "DESIGN.md" not in cites,
          f"got {list(cites)}")
    check("flags a dead frontmatter link", "Some Author" in r["frontmatter_dead_links"])
    check("flags a dead frontmatter link (markdown-style)",
          "Some Other Author" in r["frontmatter_dead_links"], f"got {list(r['frontmatter_dead_links'])}")
    check("flags backtick-only wikilinks",
          any(p.endswith("log.md") for p in r["backtick_only_references"]))
    check("flags backtick-only markdown links",
          any(p.endswith("log-md.md") for p in r["backtick_only_references"]),
          f"got {r['backtick_only_references']}")
    check("flags a case collision", len(r["case_collisions"]) == 1,
          f"got {r['case_collisions']}")
    check("flags a file in the vault root", "stray.md" in r["vault_root_files"])
    check("flags a genuinely broken link", "No Such Note" in broken)
    check("ignores links inside a code fence", "placeholder-name" not in broken)
    check("ignores data: URIs", not any("base64" in k for k in broken))
    # Exactly two links in this fixture are real: good.md -> Workshop summary,
    # and wiki-index.md -> Ingest notes (the already-linked entry in the
    # Sources-ingested list). Asserting the exact number is the point — an
    # earlier scanner counted fenced and backticked examples as edges, which
    # made a vault look far more connected than it was and hid the orphans
    # entirely. Update this number when the fixture gains a real link, never to
    # make a failure go away.
    check("counts exactly the real edges, no over-counting",
          r["counts"]["edges"] == 2, f"got {r['counts']['edges']}")
    check("reports orphans", isinstance(r["orphans"], list) and len(r["orphans"]) > 0)

    stale = {row["row_path"]: row for row in r["stale_routing_map_rows"]}
    check("does not flag a Routing Map row whose folder still exists",
          "1-Projects/Live Project/" not in stale, f"got {list(stale)}")
    check("flags a Routing Map row whose folder is gone",
          "1-Projects/Gone Project/" in stale, f"got {list(stale)}")
    check("identifies where an archived row's folder actually went",
          stale.get("1-Projects/Gone Project/", {}).get("archived_at") == "4-Archives/Old Area/Gone Project",
          f"got {stale.get('1-Projects/Gone Project/')}")
    check("flags a Routing Map row with no matching folder anywhere",
          "1-Projects/Never Existed/" in stale
          and stale["1-Projects/Never Existed/"]["archived_at"] is None)
    check("does not flag a row marked [replace on setup]",
          "2-Areas/Some Guide.md" not in stale, f"got {list(stale)}")

print()
if failures:
    print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("all checks passed")
