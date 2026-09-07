#!/usr/bin/env python3
"""Self-test for shared_content_sync.py. Builds a synthetic shared clone and
knowledge base covering the case this script exists for: a shared folder
that exists in the clone but has no symlink into the knowledge base yet,
because it was created after the knowledge base's own one-time setup ran.

Run: python test_shared_content_sync.py
"""
import os, sys, tempfile, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "shared_content_sync", os.path.join(HERE, "shared_content_sync.py"))
scs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scs)

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")


def build_clone(root):
    write(root, "Research Repository/index.md", "x\n")
    write(root, "Cashback Card/Wiki/index.md", "x\n")
    write(root, "Broadband/Wiki/index.md", "x\n")  # the new, unlinked wiki
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                     "commit", "-q", "-m", "init"], cwd=root, check=True)


def write(root, rel, text):
    full = os.path.join(root, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


with tempfile.TemporaryDirectory() as tmp:
    clone = os.path.join(tmp, "clone")
    vault = os.path.join(tmp, "vault")
    os.makedirs(clone)
    build_clone(clone)

    os.makedirs(os.path.join(vault, "2-Areas"))
    os.makedirs(os.path.join(vault, "1-Projects", "Cashback Card"))
    os.symlink(os.path.join(clone, "Research Repository"),
               os.path.join(vault, "2-Areas", "Research Repository"))
    os.symlink(os.path.join(clone, "Cashback Card", "Wiki"),
               os.path.join(vault, "1-Projects", "Cashback Card", "Wiki"))
    # Broadband/Wiki deliberately left un-symlinked.

    # find_clone_root must resolve the clone from an existing symlink alone,
    # the same way setup-my-knowledge-base leaves no other pointer to it.
    found = scs.find_clone_root(vault)
    check("finds the clone root via an existing symlink", found == os.path.realpath(clone))

    result = scs.check(vault)
    check("clone_found is True", result["clone_found"] is True)
    missing_names = {f["name"] for f in result["missing"]}
    check("flags the un-symlinked Broadband wiki", missing_names == {"Broadband"})
    check("does not flag the already-linked Research Repository",
          "Research Repository" not in missing_names)
    check("does not flag the already-linked Cashback Card wiki",
          "Cashback Card" not in missing_names)

# Add the missing symlink in a fresh copy of the same setup and confirm the
# check clears — proves this is a live re-check, not a cached verdict.
with tempfile.TemporaryDirectory() as tmp:
    clone = os.path.join(tmp, "clone")
    vault = os.path.join(tmp, "vault")
    os.makedirs(clone)
    build_clone(clone)
    os.makedirs(os.path.join(vault, "2-Areas"))
    os.makedirs(os.path.join(vault, "1-Projects", "Cashback Card"))
    os.makedirs(os.path.join(vault, "1-Projects", "Broadband"))
    os.symlink(os.path.join(clone, "Research Repository"),
               os.path.join(vault, "2-Areas", "Research Repository"))
    os.symlink(os.path.join(clone, "Cashback Card", "Wiki"),
               os.path.join(vault, "1-Projects", "Cashback Card", "Wiki"))
    os.symlink(os.path.join(clone, "Broadband", "Wiki"),
               os.path.join(vault, "1-Projects", "Broadband", "Wiki"))

    result = scs.check(vault)
    check("clears once the missing symlink is added", result["missing"] == [])

    # "everything in sync" (clone found, pull ok, nothing missing) must read
    # as a clean pass, not collapse into the same message as "no clone at
    # all" -- report() returning "" is the right signal for both, so the
    # CLI has to tell them apart using clone_found. The synthetic clone has
    # no real remote, so build a synced result by hand rather than relying
    # on a real `git pull` to succeed.
    synced = {"clone_found": True, "clone_root": clone, "pull_ok": True,
              "pull_output": "Already up to date.", "missing": []}
    check("report() is empty when everything is already linked (a real pass, not 'no clone found')",
          scs.report(synced) == "")

# No shared clone linked in at all -- must not crash, must report cleanly.
with tempfile.TemporaryDirectory() as tmp:
    vault = os.path.join(tmp, "vault")
    os.makedirs(os.path.join(vault, "2-Areas"))
    result = scs.check(vault)
    check("reports clone_found False when nothing is linked in yet",
          result == {"clone_found": False})
    check("report() returns empty string for that case", scs.report(result) == "")

if failures:
    print(f"\n{len(failures)} check(s) failed")
    sys.exit(1)
print("All checks passed.")
