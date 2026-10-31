#!/usr/bin/env python3
"""Seam pack-level #19 : vérification du pack complet.

Usage:
  python3 scripts/check-pack.py

Vérifie les 4 critères d'acceptation du ticket #19 :
- 12 domaines présents, traçabilité 135/135 au commit figé
- 12 descriptions déclenchables avec renvois explicites (skill-creator)
- renvois inter-skills cohérents (catalogue→sécurité, CLI homonymes, mobile non éclaté)
- chaque référence porte ec113a50, Rust linkée jamais copiée.

FAIL (exit 1) sur le premier écart, OK (exit 0) sinon.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED = [
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
]


def fail(msg: str) -> int:
    print(f"FAIL pack: {msg}")
    return 1


def main() -> int:
    # 1. 12 skills, pas de mobile éclaté
    for name in EXPECTED:
        if not (SKILLS / name / "SKILL.md").is_file():
            return fail(f"skill manquant: {name}")
    if (SKILLS / "tauri-mobile").exists():
        return fail("skill mobile éclaté interdit")

    # 2. descriptions déclenchables
    for name in EXPECTED:
        text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        if len(text.splitlines()) >= 500:
            return fail(f"{name}: SKILL.md >= 500 lignes")
        m = re.search(r"description:\s*(.+)", text)
        if not m:
            return fail(f"{name}: frontmatter description manquant")
        if "Use me whenever" not in m.group(1):
            return fail(f"{name}: description non pushy (Use me whenever manquant)")
        if "tauri-" not in m.group(1):
            return fail(f"{name}: description sans renvoi explicite tauri-*")

    # 3a. CLI homonymes (dev vs in-app)
    cli_ref = SKILLS / "tauri-config-cli-reference" / "references" / "cli.md"
    cli_text = cli_ref.read_text(encoding="utf-8")
    for token in ["Dev CLI", "In-app CLI", "CliExt", "getMatches"]:
        if token not in cli_text:
            return fail(f"config-cli/cli.md sans marqueur homonyme: {token}")
    desc_cli = (SKILLS / "tauri-config-cli-reference" / "SKILL.md").read_text(encoding="utf-8")
    if "dev CLI" not in desc_cli or "in-app" not in desc_cli:
        return fail("config-cli description sans homonymes dev vs in-app")

    # 3b. catalogue → sécurité sans duplication
    for ref in (SKILLS / "tauri-plugins-catalogue" / "references").glob("*.md"):
        if "tauri-security-capabilities" not in ref.read_text(encoding="utf-8"):
            return fail(f"{ref.name}: sans renvoi sécurité")

    # 3c. mobile non éclaté
    mobiles = sorted(p.parent.parent.name for p in SKILLS.glob("tauri-*/references/mobile.md"))
    if mobiles != ["tauri-plugin-dev", "tauri-ui-recettes"]:
        return fail(f"mobile éclaté ou manquant: {mobiles}")

    # 4a. pointeurs source ec113a50
    refs = list(SKILLS.glob("tauri-*/references/*.md"))
    if len(refs) < 80:
        return fail(f"références insuffisantes: {len(refs)}")
    sans = [p.name for p in refs if "ec113a50" not in p.read_text(encoding="utf-8")]
    if sans:
        return fail(f"sans pointeur ec113a50: {sans[:5]}")

    # 4b. Rust linkée (docs.rs) dans les skills à code natif
    docs_rs_refs = 0
    for skill in ["tauri-frontend-bindings", "tauri-plugin-dev", "tauri-ui-recettes"]:
        for ref in (SKILLS / skill / "references").glob("*.md"):
            if "docs.rs" in ref.read_text(encoding="utf-8"):
                docs_rs_refs += 1
    if docs_rs_refs < 5:
        return fail(f"Rust linkée insuffisante (docs.rs dans {docs_rs_refs} refs)")

    # 5. traçabilité 135/135 au commit figé
    traca = ROOT / "docs" / "tracabilite.json"
    data = json.loads(traca.read_text(encoding="utf-8"))
    if data.get("commit") != "ec113a50":
        return fail("tracabilite.json commit != ec113a50")
    if len(data.get("mapping", {})) != 135:
        return fail(f"tracabilite.json != 135 pages: {len(data.get('mapping', {}))}")

    # 6. evals skill-creator présents (2-3 prompts par skill)
    for name in EXPECTED:
        evals = SKILLS / name / "evals" / "evals.json"
        if not evals.is_file():
            return fail(f"{name}: evals/evals.json manquant")
        n = len(json.loads(evals.read_text(encoding="utf-8")).get("evals", []))
        if n < 2:
            return fail(f"{name}: evals insuffisants ({n})")

    print(f"OK pack: 12/12 skills, {len(refs)} refs ec113a50, 135/135 tracées, renvois OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
