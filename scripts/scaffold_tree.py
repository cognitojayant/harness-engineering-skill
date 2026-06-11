#!/usr/bin/env python3
"""Scaffold the harness documentation tree (directories only).

Creates only the directories the chosen docs need (idempotent) and a .gitkeep in
each leaf dir that holds no files yet. It deliberately does NOT create the doc
files themselves — the caller writes each file's content directly with the Write
tool. (Pre-creating empty files forces an extra Read-before-Write round-trip,
which this avoids.) It prints the list of files you should author next.

Usage:
    scaffold_tree.py --root <repo-root> --manifest agents,architecture,security,...

Manifest keys map to files/subtrees as defined in references/doc-catalog.md.
Pass only the keys for docs the project warrants (adaptive doc set).
"""
import argparse
import os
import sys

# key -> list of paths (relative to repo root). Directories end with "/".
LAYOUT = {
    "agents": ["AGENTS.md"],
    "architecture": ["ARCHITECTURE.md"],
    "design": ["docs/DESIGN.md"],
    "frontend": ["docs/FRONTEND.md"],
    "plans": ["docs/PLANS.md"],
    "product_sense": ["docs/PRODUCT_SENSE.md"],
    "quality_score": ["docs/QUALITY_SCORE.md"],
    "reliability": ["docs/RELIABILITY.md"],
    "security": ["docs/SECURITY.md"],
    "design_docs": ["docs/design-docs/index.md", "docs/design-docs/core-beliefs.md"],
    "exec_plans": [
        "docs/exec-plans/active/",
        "docs/exec-plans/completed/",
        "docs/exec-plans/tech-debt-tracker.md",
    ],
    "generated": ["docs/generated/db-schema.md"],
    "research": ["docs/research/Research.md"],
    "product_specs": [
        "docs/product-specs/index.md",
        "docs/product-specs/new-user-onboarding.md",
    ],
    "references": ["docs/references/"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="repo root")
    ap.add_argument(
        "--manifest",
        required=True,
        help="comma-separated doc keys (see doc-catalog.md)",
    )
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit(f"error: root is not a directory: {root}")

    keys = [k.strip() for k in args.manifest.split(",") if k.strip()]
    unknown = [k for k in keys if k not in LAYOUT]
    if unknown:
        sys.exit(f"error: unknown manifest keys: {unknown}\nvalid: {sorted(LAYOUT)}")

    dirs_made = []          # directories actually created
    files_to_author = []    # doc files the caller must Write
    files_existing = []     # doc files already present (update mode)

    for key in keys:
        for rel in LAYOUT[key]:
            path = os.path.join(root, rel)
            if rel.endswith("/"):
                # explicit empty dir (e.g. exec-plans/active/) — keep it in git
                if not os.path.isdir(path):
                    os.makedirs(path, exist_ok=True)
                    dirs_made.append(rel)
                gk = os.path.join(path, ".gitkeep")
                if not os.listdir(path):
                    open(gk, "a").close()
            else:
                parent = os.path.dirname(path)
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent, exist_ok=True)
                    dirs_made.append(os.path.relpath(parent, root) + "/")
                (files_existing if os.path.exists(path) else files_to_author).append(rel)

    print(f"root: {root}")
    print(f"directories ensured ({len(dirs_made)}):")
    for d in sorted(set(dirs_made)):
        print(f"  + {d}")
    print(f"\nfiles to AUTHOR now with the Write tool ({len(files_to_author)}):")
    for f in files_to_author:
        print(f"  > {f}")
    if files_existing:
        print(f"\nalready exist — update in place, don't overwrite blindly ({len(files_existing)}):")
        for f in files_existing:
            print(f"  = {f}")
    print("\nnext: write each listed file with verified content (see templates.md).")


if __name__ == "__main__":
    main()
