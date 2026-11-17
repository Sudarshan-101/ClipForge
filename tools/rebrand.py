#!/usr/bin/env python3
"""Rename the product everywhere (display name, lowercase slug, UPPERCASE env prefix).

    python tools/rebrand.py . --old ClipForge --name YourName

Skips LICENSE and the fonts folder. Rename the nginx config file and re-run
tools/make_logos.py yourself if you also want new logo files.
"""
import argparse, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("root")
ap.add_argument("--old", required=True, help="Current name, e.g. ClipForge")
ap.add_argument("--name", required=True, help="New name")
a = ap.parse_args()

TEXT_EXT = {".py", ".md", ".html", ".js", ".yml", ".yaml", ".txt", ".conf", ".example", ".svg", ".toml", ""}
SKIP_DIRS = {".git", "fonts", "node_modules"}
pairs = [(a.old, a.name), (a.old.upper(), a.name.upper()), (a.old.lower(), a.name.lower())]

changed = 0
root = pathlib.Path(a.root)
for p in root.rglob("*"):
    if not p.is_file() or SKIP_DIRS & set(p.relative_to(root).parts) or p.name == "LICENSE":
        continue
    if p.suffix.lower() not in TEXT_EXT and p.name not in {".env.example", "Dockerfile", ".dockerignore"}:
        continue
    try:
        t = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    o = t
    for old, new in pairs:
        t = t.replace(old, new)
    if t != o:
        p.write_text(t, encoding="utf-8")
        changed += 1
print("files changed:", changed)
