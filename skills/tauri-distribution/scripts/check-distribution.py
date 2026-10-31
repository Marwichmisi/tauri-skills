#!/usr/bin/env python3
"""Check déterministe distribution Tauri v2 (seam basse tauri-distribution).

Valide le comportement externe de l'agent sur des artefacts reproductibles
fidèles à la doc locale commit ec113a50 (EN canonique seule), sans inventer
de bundle target ni de variable de signature. Ne prouve PAS à lui seul la
couverture doc : les pointeurs source se vérifient dans la réponse.

Règles issues de tauri-docs :
- updater : bundle.createUpdaterArtifacts true|"v1Compatible", plugins.updater.pubkey
  non-vide et non-chemin (doc : "cannot be a file path"), endpoints[] https sauf
  dangerousInsecureTransportProtocol true, installMode windows passive|basicUi|quiet.
- bundle : targets documentés seuls (app,dmg,msi,nsis,deb,rpm,appimage) via
  bundle.targets JSON ou chaîne --bundles "app,dmg".
- sign : noms de variables documentées seules (TAURI_SIGNING_*, APPLE_*,
  WINDOWS_*, IOS_*, SIGN/SIGN_KEY/APPIMAGETOOL_*).

Usage :
  python3 scripts/check-distribution.py --updater examples/tauri.conf.updater.json
  python3 scripts/check-distribution.py --bundle examples/tauri.conf.bundle.json
  python3 scripts/check-distribution.py --sign examples/signing.env
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

BUNDLE_ALLOWED = {"app", "dmg", "msi", "nsis", "deb", "rpm", "appimage"}
INSTALL_MODES = {"passive", "basicUi", "quiet"}
SIGN_ALLOWED = {
    "TAURI_SIGNING_PRIVATE_KEY",
    "TAURI_SIGNING_PRIVATE_KEY_PASSWORD",
    "APPLE_SIGNING_IDENTITY",
    "APPLE_CERTIFICATE",
    "APPLE_CERTIFICATE_PASSWORD",
    "APPLE_ID",
    "APPLE_PASSWORD",
    "APPLE_TEAM_ID",
    "APPLE_API_ISSUER",
    "APPLE_API_KEY",
    "APPLE_API_KEY_PATH",
    "WINDOWS_CERTIFICATE",
    "WINDOWS_CERTIFICATE_PASSWORD",
    "WINDOWS_PFX_PASSWORD",
    "IOS_CERTIFICATE",
    "IOS_CERTIFICATE_PASSWORD",
    "IOS_MOBILE_PROVISION",
    "SIGN",
    "SIGN_KEY",
    "APPIMAGETOOL_SIGN_PASSPHRASE",
    "APPIMAGETOOL_FORCE_SIGN",
    "GITHUB_TOKEN",
}


ALLOWED_TARGET_VAR = {"{{target}}", "{{arch}}", "{{current_version}}"}


def is_path_like(pubkey: str) -> bool:
    p = pubkey.strip()
    return p.endswith(".pem") or "/" in p or "\\" in p or p.startswith("./")


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def check_updater(path: pathlib.Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"{path}: JSON illisible ({e})")
    errors: list[str] = []
    bundle = data.get("bundle", {})
    cua = bundle.get("createUpdaterArtifacts")
    if cua not in (True, "v1Compatible"):
        errors.append(
            "bundle.createUpdaterArtifacts doit être true ou 'v1Compatible' "
            "(plugin/updater.mdx)"
        )
    plugins = data.get("plugins", {})
    updater = plugins.get("updater")
    if not isinstance(updater, dict):
        errors.append("plugins.updater manquant (plugin/updater.mdx)")
        updater = {}
    pubkey = updater.get("pubkey", "")
    if not isinstance(pubkey, str) or len(pubkey.strip()) < 16:
        errors.append("plugins.updater.pubkey manquant ou trop court")
    elif is_path_like(pubkey):
        errors.append(
            "plugins.updater.pubkey ne peut pas être un chemin de fichier "
            "(doc : cannot be a file path)"
        )
    endpoints = updater.get("endpoints")
    if not isinstance(endpoints, list) or not endpoints:
        errors.append("plugins.updater.endpoints doit être un tableau non vide")
    else:
        insecure = updater.get("dangerousInsecureTransportProtocol") is True
        for ep in endpoints:
            if not isinstance(ep, str) or not ep:
                errors.append(f"endpoint invalide: {ep!r}")
                continue
            if not (ep.startswith("https://") or ep.startswith("http://")):
                # variables dynamiques seules autorisées, pas de custom
                if "{{" in ep:
                    for m in re.finditer(r"\{\{[^}]+\}\}", ep):
                        if m.group(0) not in ALLOWED_TARGET_VAR:
                            errors.append(
                                f"variable custom non supportée: {m.group(0)} "
                                "(target/arch/current_version seuls)"
                            )
                else:
                    errors.append(f"endpoint doit être une URL: {ep!r}")
            elif ep.startswith("http://") and not insecure:
                errors.append(
                    f"endpoint non-HTTPS sans dangerousInsecureTransportProtocol: {ep!r}"
                )
    win = updater.get("windows", {})
    if isinstance(win, dict) and "installMode" in win:
        if win["installMode"] not in INSTALL_MODES:
            errors.append(
                f"windows.installMode invalide: {win['installMode']!r} "
                "(passive|basicUi|quiet)"
            )
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: updater pubkey + {len(endpoints)} endpoint(s) https")
    return 0


def check_bundle(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8").strip()
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    targets: list[str] = []
    try:
        data = json.loads(text)
    except Exception as e:
        return fail(f"{path}: JSON illisible ({e})")
    bundle = data.get("bundle", {})
    if not isinstance(bundle, dict):
        return fail(f"{path}: bundle doit être un objet")
    raw = bundle.get("targets", [])
    if isinstance(raw, str):
        targets = [t.strip() for t in raw.split(",") if t.strip()]
    elif isinstance(raw, list):
        targets = raw
    else:
        return fail(f"{path}: bundle.targets doit être liste ou chaîne")
    errors = []
    if not targets:
        errors.append("aucun bundle target (ex: app,dmg)")
    for t in targets:
        if t not in BUNDLE_ALLOWED:
            errors.append(
                f"bundle target inventé: {t!r} "
                f"(documentés: {sorted(BUNDLE_ALLOWED)})"
            )
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: targets={','.join(targets)}")
    return 0


def check_sign(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    names: list[str] = []
    for m in re.finditer(r"^([A-Z][A-Z0-9_]+)\s*[:=]", text, re.M):
        names.append(m.group(1))
    for m in re.finditer(r"\$\{\{\s*secrets\.([A-Z0-9_]+)\s*\}\}", text):
        names.append(m.group(1))
    for m in re.finditer(r"\$env:([A-Z0-9_]+)", text):
        names.append(m.group(1))
    # déduplique en gardant l'ordre
    seen: list[str] = []
    for n in names:
        if n not in seen:
            seen.append(n)
    if not seen:
        return fail(f"{path}: aucune variable de signature trouvée")
    errors = [f"variable de signature inventée: {n!r}" for n in seen if n not in SIGN_ALLOWED]
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: vars={','.join(seen)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--updater", dest="updater")
    ap.add_argument("--bundle", dest="bundle")
    ap.add_argument("--sign", dest="sign")
    args = ap.parse_args()
    if args.updater:
        return check_updater(pathlib.Path(args.updater))
    if args.bundle:
        return check_bundle(pathlib.Path(args.bundle))
    if args.sign:
        return check_sign(pathlib.Path(args.sign))
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
