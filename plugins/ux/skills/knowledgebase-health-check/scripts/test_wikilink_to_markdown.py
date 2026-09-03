#!/usr/bin/env python3
"""Self-test for wikilink_to_markdown.py. Builds a small synthetic repo
covering every conversion case and the traps that made an earlier hand-rolled
attempt at this dangerous: code fences, name collisions, escaped-pipe table
rows, '#' inside an alias, and stale 2-Areas/ prefixes.

Run: python test_wikilink_to_markdown.py
"""
import os, sys, tempfile, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vl = load("vault_lint")
w2m = load("wikilink_to_markdown")

FILES = {
    # plain bare-stem wikilink, resolves within the same folder
    "AreaA/Wiki/page-a.md": "See [[page-b]] for more.\n",
    "AreaA/Wiki/page-b.md": "target page\n",

    # piped alias -- display text must be the alias, not the target
    "AreaA/Wiki/aliased.md": "Read [[page-b|the other page]] first.\n",

    # cross-area resolution: source in AreaB links to a page that only
    # exists in AreaA -- must resolve repo-wide, and the computed relative
    # path must actually cross the area boundary correctly
    "AreaB/Wiki/linker.md": "Related: [[page-b]].\n",

    # a target that doesn't exist anywhere in this repo (a private-vault-only
    # source) -- must be left completely untouched
    "AreaA/Wiki/vaultonly.md": "See [[Some Private Transcript]] for detail.\n",

    # the canary: a wikilink inside inline backticks on the same line as a
    # real one -- only the real one may convert
    "AreaA/Wiki/log.md": "changed `[[page-b]]` today, see also [[page-a]]\n",

    # a wikilink inside a fenced code block -- must not convert, must not
    # even be seen as a candidate
    "AreaA/Wiki/spec.md": "Example:\n\n```markdown\n[[page-b]]\n```\n",

    # '#' inside an alias, not the target -- must survive as literal text,
    # never treated as a heading anchor or a split point
    "AreaA/Wiki/hashalias.md": "[[page-b|research gap #1]] and more\n",

    # a genuine name collision: two files share a stem, in different folders.
    # The linking file sits in the SAME folder as one of the two candidates
    # (mirrors the real Partner Survey stub/report pair) -- must stay
    # ambiguous and untouched, not silently resolve to the same-folder one.
    "AreaA/Studies/dup-linker.md": "Full report: [[Dup Name]]\n",
    "AreaA/Studies/Dup Name.md": "\n",
    "AreaA/Reports/Dup Name.md": "the real, full report\n",

    # escaped-pipe wikilink in a table row, target unresolvable -- the whole
    # row must be byte-identical after conversion (the hardest real case:
    # every escaped-pipe instance in the real repo is vault-only)
    "AreaA/Reports/report.md": (
        "| Row | Link |\n|---|---|\n"
        "| a | [[2026-05-07 Someone — Cleaned Transcript\\|Cleaned]] |\n"
    ),

    # a stale vault-rooted path baked into the link text -- must resolve
    # after stripping the leading "2-Areas/", not before
    "AreaA/Wiki/rerooted.md": "See [[2-Areas/AreaA/index|the index]].\n",
    "AreaA/index.md": "area index\n",

    # image embed -- bang must be preserved, target resolves via attachments
    "AreaA/Wiki/embed.md": "![[photo.png]]\n",
    "AreaA/Wiki/photo.png": "binary\n",

    # image embed whose target doesn't exist in this repo -- untouched
    "AreaA/Reports/embed-missing.md": "![[not-here.jpg]]\n",

    # a filename needing percent-encoding in the output path, but not in the
    # display text
    "AreaA/Wiki/encode-target.md": "See [[Weird (Name) #2]].\n",
    "AreaA/Wiki/Weird (Name) #2.md": "weird file\n",
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

    vault = vl.Vault(root)
    results = {}
    for p in vault.md:
        new_text, changed, changes = w2m.convert_file(vault, p)
        results[p] = (new_text, changed, changes)

    # --- plain bare-stem conversion ---
    new_text, changed, changes = results["AreaA/Wiki/page-a.md"]
    check("converts a plain bare-stem wikilink", changed)
    check("output uses markdown link syntax", "[page-b](page-b.md)" in new_text,
          f"got {new_text!r}")
    check("original wikilink is gone", "[[page-b]]" not in new_text)

    # --- alias becomes display text ---
    new_text, changed, changes = results["AreaA/Wiki/aliased.md"]
    check("uses the alias as display text, not the raw target",
          "[the other page](page-b.md)" in new_text, f"got {new_text!r}")

    # --- cross-area resolution ---
    new_text, changed, changes = results["AreaB/Wiki/linker.md"]
    check("resolves a cross-area target repo-wide", changed)
    check("computes the correct relative path across areas",
          "[page-b](../../AreaA/Wiki/page-b.md)" in new_text, f"got {new_text!r}")

    # --- vault-only target left untouched ---
    new_text, changed, changes = results["AreaA/Wiki/vaultonly.md"]
    check("leaves a vault-only target completely untouched", not changed)
    check("vault-only wikilink survives byte-for-byte",
          new_text == FILES["AreaA/Wiki/vaultonly.md"])

    # --- canary: backticked link stays, real link on the same line converts ---
    new_text, changed, changes = results["AreaA/Wiki/log.md"]
    check("canary: backticked wikilink is untouched",
          "`[[page-b]]`" in new_text, f"got {new_text!r}")
    check("canary: the real link on the same line still converts",
          "[page-a](page-a.md)" in new_text, f"got {new_text!r}")

    # --- fenced code block: no conversion, not even detected ---
    new_text, changed, changes = results["AreaA/Wiki/spec.md"]
    check("a wikilink inside a fenced code block is not converted", not changed)
    check("fenced example is untouched byte-for-byte",
          new_text == FILES["AreaA/Wiki/spec.md"])

    # --- '#' inside an alias survives; never a split point ---
    new_text, changed, changes = results["AreaA/Wiki/hashalias.md"]
    check("'#' inside an alias is preserved, not split on",
          "[research gap #1](page-b.md)" in new_text, f"got {new_text!r}")

    # --- name collision: refuse to guess ---
    new_text, changed, changes = results["AreaA/Studies/dup-linker.md"]
    check("a genuine name collision is left untouched, not resolved to the "
          "same-folder candidate", not changed)
    check("colliding wikilink survives byte-for-byte",
          new_text == FILES["AreaA/Studies/dup-linker.md"])

    # --- escaped-pipe table row: byte-identical, hardest real case ---
    new_text, changed, changes = results["AreaA/Reports/report.md"]
    check("an escaped-pipe wikilink to an unresolvable target leaves the "
          "whole file byte-identical", new_text == FILES["AreaA/Reports/report.md"],
          f"got {new_text!r}")

    # --- stale 2-Areas/ prefix: strip and retry ---
    new_text, changed, changes = results["AreaA/Wiki/rerooted.md"]
    check("resolves after stripping a stale 2-Areas/ prefix", changed)
    check("re-rooted link points at the real repo-relative path",
          "[the index](../index.md)" in new_text, f"got {new_text!r}")
    check("re-root is reported with its own status",
          changes and changes[0]["status"] == "ok-reroot", f"got {changes}")

    # --- image embeds ---
    new_text, changed, changes = results["AreaA/Wiki/embed.md"]
    check("image embed keeps its leading '!' and converts via attachments",
          "![photo.png](photo.png)" in new_text, f"got {new_text!r}")

    new_text, changed, changes = results["AreaA/Reports/embed-missing.md"]
    check("an image embed with no matching file is left untouched", not changed)

    # --- encoding: only the six required characters, in the path only ---
    new_text, changed, changes = results["AreaA/Wiki/encode-target.md"]
    check("display text is not percent-encoded",
          "[Weird (Name) #2]" in new_text, f"got {new_text!r}")
    check("path is percent-encoded for space, parens, and hash",
          "(Weird%20%28Name%29%20%232.md)" in new_text, f"got {new_text!r}")

    # --- dry-run vs --write ---
    before = open(os.path.join(root, "AreaA/Wiki/page-a.md"), encoding="utf-8").read()
    check("dry run: file on disk is untouched before --write",
          "[[page-b]]" in before)

    import subprocess
    subprocess.run([sys.executable, os.path.join(HERE, "wikilink_to_markdown.py"),
                     root, "--write"], check=True, capture_output=True, text=True)
    after = open(os.path.join(root, "AreaA/Wiki/page-a.md"), encoding="utf-8").read()
    check("--write actually rewrites the file on disk",
          "[page-b](page-b.md)" in after, f"got {after!r}")
    untouched_after = open(os.path.join(root, "AreaA/Studies/dup-linker.md"), encoding="utf-8").read()
    check("--write does not touch files with nothing to convert",
          untouched_after == FILES["AreaA/Studies/dup-linker.md"])

    # --- '#' in a target that doesn't match anything real: left untouched,
    # not treated as heading-anchor syntax the script doesn't parse ---
    resolved, status = w2m.resolve(vault, "page-b#Heading")
    check("a target with '#' that matches nothing is left unresolved, not guessed",
          resolved is None and status == 'not-found', f"got {(resolved, status)}")

print()
if failures:
    print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("all checks passed")
