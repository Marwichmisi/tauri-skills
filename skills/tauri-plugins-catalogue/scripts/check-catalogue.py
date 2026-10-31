#!/usr/bin/env python3
"""Check déterministe catalogue plugins Tauri v2 (seam basse tauri-plugins-catalogue).

Valide le comportement externe de l'agent sur un routage 1-étape + capability
fidèle à la doc locale commit ec113a50 (EN canonique seule), sans inventer
de permission. Ne prouve PAS à lui seul la couverture doc : les pointeurs
source (fichier + commit + titre) se vérifient dans la réponse, exigés par
les expectations d'eval.

Règles issues de tauri-docs :
- 30 fiches plugin/** hors updater (updater vit dans tauri-distribution).
- permission format : plugin:perm / plugin:scope:cle ou set nu kébab
  (même PERM_RE que tauri-security-capabilities), préfixe connu uniquement
  (30 préfixes catalogue + core), updater: rejeté avec renvoi distribution.
- JS guest : @tauri-apps/plugin-<npm> du plugin ciblé (sauf Rust-only :
  localhost, persisted-scope, single-instance, et overview routeur).

Usage :
  python3 scripts/check-catalogue.py --list
  python3 scripts/check-catalogue.py --plugin file-system --capability examples/capability-fs.json
  python3 scripts/check-catalogue.py --plugin dialog --js examples/dialog.js --capability examples/capability-dialog.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

PERM_RE = re.compile(
    r"^(?:[a-z0-9-]+:[a-z0-9-*]+(?::[a-z0-9-*]+)?|[a-z0-9]+-[a-z0-9-]+)$"
)

# slug (nom fiche / référence) -> {prefix (permission), npm (tauri add), js (guest-js)}
CATALOGUE: dict[str, dict[str, str | None]] = {
    "autostart": {"prefix": "autostart", "npm": "autostart", "js": "autostart"},
    "barcode-scanner": {"prefix": "barcode-scanner", "npm": "barcode-scanner", "js": "barcode-scanner"},
    "biometric": {"prefix": "biometric", "npm": "biometric", "js": "biometric"},
    "cli": {"prefix": "cli", "npm": "cli", "js": "cli"},
    "clipboard": {"prefix": "clipboard-manager", "npm": "clipboard-manager", "js": "clipboard-manager"},
    "deep-linking": {"prefix": "deep-link", "npm": "deep-link", "js": "deep-link"},
    "dialog": {"prefix": "dialog", "npm": "dialog", "js": "dialog"},
    "file-system": {"prefix": "fs", "npm": "fs", "js": "fs"},
    "geolocation": {"prefix": "geolocation", "npm": "geolocation", "js": "geolocation"},
    "global-shortcut": {"prefix": "global-shortcut", "npm": "global-shortcut", "js": "global-shortcut"},
    "haptics": {"prefix": "haptics", "npm": "haptics", "js": "haptics"},
    "http-client": {"prefix": "http", "npm": "http", "js": "http"},
    "overview": {"prefix": None, "npm": None, "js": None},
    "localhost": {"prefix": "localhost", "npm": "localhost", "js": None},
    "logging": {"prefix": "log", "npm": "log", "js": "log"},
    "nfc": {"prefix": "nfc", "npm": "nfc", "js": "nfc"},
    "notification": {"prefix": "notification", "npm": "notification", "js": "notification"},
    "opener": {"prefix": "opener", "npm": "opener", "js": "opener"},
    "os-info": {"prefix": "os", "npm": "os", "js": "os"},
    "persisted-scope": {"prefix": "persisted-scope", "npm": "persisted-scope", "js": None},
    "positioner": {"prefix": "positioner", "npm": "positioner", "js": "positioner"},
    "process": {"prefix": "process", "npm": "process", "js": "process"},
    "shell": {"prefix": "shell", "npm": "shell", "js": "shell"},
    "single-instance": {"prefix": "single-instance", "npm": "single-instance", "js": None},
    "sql": {"prefix": "sql", "npm": "sql", "js": "sql"},
    "store": {"prefix": "store", "npm": "store", "js": "store"},
    "stronghold": {"prefix": "stronghold", "npm": "stronghold", "js": "stronghold"},
    "upload": {"prefix": "upload", "npm": "upload", "js": "upload"},
    "websocket": {"prefix": "websocket", "npm": "websocket", "js": "websocket"},
    "window-state": {"prefix": "window-state", "npm": "window-state", "js": "window-state"},
}

KNOWN_PREFIXES = {v["prefix"] for v in CATALOGUE.values() if v["prefix"]} | {"core"}


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def check_capability(path: pathlib.Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{path}: JSON illisible ({e})"], []
    if not data.get("identifier"):
        errors.append("missing 'identifier' (capabilities/*.json doc)")
    if not data.get("windows") and not data.get("webviews"):
        errors.append("missing 'windows' or 'webviews' (capability cible requise)")
    perms = data.get("permissions")
    if not isinstance(perms, list) or not perms:
        errors.append("missing non-empty 'permissions' list")
    else:
        for p in perms:
            if not isinstance(p, str) or not PERM_RE.match(p):
                errors.append(
                    f"bad permission format: {p!r} "
                    "(attendu plugin:scope:cle, ex fs:default, ou set kébab)"
                )
                continue
            if ":" in p:
                prefix = p.split(":")[0]
                if prefix == "updater":
                    errors.append(
                        "permission 'updater:*' interdite ici : "
                        "plugin/updater.mdx vit dans tauri-distribution, "
                        "pas dans le catalogue"
                    )
                elif prefix not in KNOWN_PREFIXES:
                    errors.append(
                        f"préfixe permission inconnu: {prefix!r} dans {p!r} "
                        f"(connus: {sorted(KNOWN_PREFIXES)}) — "
                        "n'invente aucune permission, lis la #permission-table "
                        "de la fiche puis remonte à tauri-security-capabilities"
                    )
                else:
                    info.append(f"permission {p} (préfixe {prefix})")
            else:
                info.append(f"set {p}")
    return errors, info


def check_js(path: pathlib.Path, slug: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []
    try:
        txt = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{path}: illisible ({e})"], []
    meta = CATALOGUE[slug]
    expected = meta["js"]
    if expected is None:
        # Rust-only ou routeur : pas d'API guest-js exigée
        info.append(f"js {path.name} accepté (fiche {slug} Rust-only/routeur, pas de guest-js exigé)")
        return errors, info
    needle = f"@tauri-apps/plugin-{expected}"
    alt = f"plugin:{meta['prefix']}|"
    if needle in txt or alt in txt:
        info.append(f"js importe {needle}")
    else:
        # détecte un mauvais plugin pour message actionnable
        m = re.search(r"@tauri-apps/plugin-([a-z-]+)", txt)
        found = m.group(1) if m else "?"
        errors.append(
            f"js {path.name} n'importe pas le plugin {slug!r} "
            f"(attendu {needle}, vu plugin-{found}) — "
            f"mauvaise fiche, relis le tableau de routage SKILL.md"
        )
    return errors, info


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="liste les 30 fiches")
    ap.add_argument("--plugin", default=None, help="slug fiche (ex file-system)")
    ap.add_argument("--js", default=None, help="snippet frontend guest-js")
    ap.add_argument("--capability", default=None, help="capability JSON à valider")
    args = ap.parse_args(argv)

    if args.list:
        for slug in sorted(CATALOGUE):
            print(slug)
        return 0

    if not args.plugin:
        print("FAIL: --plugin requis (ou --list)")
        return 1
    slug = args.plugin
    if slug == "updater":
        return fail(
            "fiche 'updater' hors catalogue : plugin/updater.mdx vit dans "
            "tauri-distribution (pipelines-updater) — "
            "renvoie vers tauri-distribution, pas vers le catalogue"
        )
    if slug not in CATALOGUE:
        return fail(
            f"fiche inconnue {slug!r} (connues: {sorted(CATALOGUE)}) — "
            "routage en une étape via SKILL.md, n'invente aucune fiche"
        )
    if not args.capability and not args.js:
        print(f"OK fiche {slug}: routage valide (préfixe {CATALOGUE[slug]['prefix']})")
        return 0

    errors: list[str] = []
    infos: list[str] = []
    if args.capability:
        cap_errs, cap_infos = check_capability(pathlib.Path(args.capability))
        errors.extend(cap_errs)
        infos.extend(cap_infos)
        target = CATALOGUE[slug]["prefix"]
        if target is not None and not cap_errs:
            try:
                data = json.loads(pathlib.Path(args.capability).read_text(encoding="utf-8"))
                perms = data.get("permissions", [])
                if not any(
                    isinstance(p, str) and ":" in p and p.split(":")[0] == target
                    for p in perms
                ):
                    infos.append(
                        f"note: aucune permission au préfixe '{target}' "
                        f"dans {args.capability} — vérifie que {slug!r} "
                        "est la bonne fiche (capability multi-plugin légitime possible)"
                    )
            except Exception:
                pass
    if args.js:
        js_errs, js_infos = check_js(pathlib.Path(args.js), slug)
        errors.extend(js_errs)
        infos.extend(js_infos)

    if errors:
        print(f"FAIL {slug} {args.capability}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {slug}: capability valide, aucune permission inventée")
    for i in infos:
        print(f" - {i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
