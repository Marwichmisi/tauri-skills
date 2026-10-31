#!/usr/bin/env python3
"""Seam haute pack-level : check de traçabilité 135 pages → domaines.

Usage:
  python3 scripts/check-tracabilite.py [--docs-root PATH] [--mapping PATH]

Comportement :
- scanne les pages EN canoniques (tauri-docs/src/content/docs, hors
  traductions de/es/fr/ja/zh-cn et hors blog/)
- charge docs/tracabilite.json (commit figé ec113a50)
- FAIL (exit 1) si une page sur disque n'est couverte par aucun domaine,
  ou si le mapping référence une page absente, ou un domaine inconnu.
- OK (exit 0) sur le mapping initial 135 → 12 domaines + hors-pack.

`hors-pack` est un état tracé explicite (about, contribute, racine,
_fragments — décision #3), pas une absence de couverture.
`tauri-frontend-bindings` couvre 0 page locale (JS généré + docs.rs linkés).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

ALLOWED = {
    "tauri-start",
    "tauri-migrate",
    "tauri-core-concepts",
    "tauri-security-capabilities",
    "tauri-ipc-bridge",
    "tauri-dev-quality",
    "tauri-plugin-dev",
    "tauri-distribution",
    "tauri-ui-recettes",
    "tauri-plugins-catalogue",
    "tauri-config-cli-reference",
    "tauri-frontend-bindings",
    "hors-pack",
}

EXCLUDED_TOP = {"de", "es", "fr", "ja", "zh-cn", "blog"}


def scan_docs(docs_root: pathlib.Path) -> list[str]:
    pages: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(docs_root):
        for fn in filenames:
            if not (fn.endswith(".mdx") or fn.endswith(".md")):
                continue
            full = pathlib.Path(dirpath) / fn
            rel = full.relative_to(docs_root).as_posix()
            top = rel.split("/")[0] if "/" in rel else rel
            # racine autorisée (index, 404, rss) : top est le fichier lui-même
            if "/" in rel and top in EXCLUDED_TOP:
                continue
            if rel.startswith("blog/"):
                continue
            pages.append(rel)
    return sorted(pages)


def main() -> int:
    here = pathlib.Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-root", default=str(here / "tauri-docs" / "src" / "content" / "docs"))
    ap.add_argument("--mapping", default=str(here / "docs" / "tracabilite.json"))
    args = ap.parse_args()

    docs_root = pathlib.Path(args.docs_root)
    mapping_path = pathlib.Path(args.mapping)

    if not docs_root.is_dir():
        print(f"FAIL docs-root introuvable: {docs_root}")
        return 1
    if not mapping_path.is_file():
        print(f"FAIL mapping introuvable: {mapping_path}")
        return 1

    data = json.loads(mapping_path.read_text(encoding="utf-8"))
    mapping: dict = data.get("mapping", {})
    commit = data.get("commit", "?")

    on_disk = scan_docs(docs_root)
    errors: list[str] = []

    for page in on_disk:
        if page not in mapping:
            errors.append(f"non couverte: {page}")

    for path, skill in mapping.items():
        if skill not in ALLOWED:
            errors.append(f"domaine inconnu: {path} → {skill!r}")
        if (docs_root / path).is_file() is False:
            # page tracée mais absente du disque (drift de commit ?)
            errors.append(f"tracée mais absente: {path}")

    # Comptes par domaine (informatif)
    from collections import Counter

    counts = Counter(mapping.values())

    if errors:
        print(f"FAIL traçabilité (commit {commit}) : {len(errors)} problème(s)")
        for e in sorted(errors)[:30]:
            print(f" - {e}")
        if len(errors) > 30:
            print(f" ... +{len(errors) - 30} autres")
        return 1

    total = len(on_disk)
    print(f"OK traçabilité {total}/{len(mapping)} (commit {commit})")
    for skill in sorted(counts):
        print(f" - {skill}: {counts[skill]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
