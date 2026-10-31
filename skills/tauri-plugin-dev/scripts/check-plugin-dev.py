#!/usr/bin/env python3
"""Check déterministe plugin Tauri v2 desktop+mobile (seam basse tauri-plugin-dev).

Valide le comportement externe de l'agent sur un squelette fidèle à la doc
locale, sans inventer d'identifiant, de permission, de plateforme ou d'invoke.
Ne prouve PAS à lui seul la couverture doc : les pointeurs source (fichier +
commit + titre) se vérifient dans la réponse, exigés par les expectations
d'eval.

Règles issues de tauri-docs commit ec113a50 (EN canonique seule) :
- identifier : [a-z0-9-], pas leading/trailing '-', un seul ':' avec préfixe,
  <=64 base / <=129 total (develop/Plugins/index.mdx, tableau + erreur build).
- permission TOML : "$schema" = "schemas/schema.json", [[permission]] avec
  identifier valide, commands.allow/deny snake_case, scope allow/deny seuls,
  [[set]]/[default] avec permissions = [identifiers valides].
- cargo : [package.metadata.platforms.support] plateformes windows/linux/
  macos/android/ios seules, level full/partial/none, notes string optionnel.
- invoke : guest-js invoke('plugin:<nom>|<cmd>'), Rust Builder::new("<nom>"),
  run_mobile_plugin("Cmd"), addPluginListener('<nom>', '<event>') ; tout
  invoke plugin-js exige le préfixe plugin:.

Usage :
  python3 scripts/check-plugin-dev.py --identifier my-plugin
  python3 scripts/check-plugin-dev.py --permission examples/permission-allow-start-server.toml
  python3 scripts/check-plugin-dev.py --cargo examples/Cargo.plugin.toml
  python3 scripts/check-plugin-dev.py --invoke examples/guest-js-upload.js
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11 fallback
    import tomli as tomllib  # type: ignore[no-redef]

BASE_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$|^[a-z0-9]$")
CMD_RE = re.compile(r"^[a-z][a-z0-9_]*$")
MOBILE_CMD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
PLUGIN_INVOKE_RE = re.compile(r"plugin:([A-Za-z0-9_.\-]+)\|([A-Za-z0-9_\-]+)")
BUILDER_RE = re.compile(r'Builder::new\(\s*"([^"]+)"')
RUN_MOBILE_RE = re.compile(r'run_mobile_plugin(?:::<[^>]+>)?\(\s*"([^"]+)"')
LISTENER_RE = re.compile(r"addPluginListener\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]")
KOTLIN_PLUGIN_RE = re.compile(r"@TauriPlugin\b")
KOTLIN_CMD_RE = re.compile(r"@Command\b\s*\n?\s*fun\s+([A-Za-z][A-Za-z0-9_]*)")
SWIFT_CMD_RE = re.compile(r"@objc[^\n]*func\s+([A-Za-z][A-Za-z0-9_]*)\s*\(\s*_\s*invoke\s*:\s*Invoke")
TRIGGER_RE = re.compile(r"""trigger\s*\(\s*["']([^"']+)["']""")
BARE_INVOKE_RE = re.compile(r"""invoke\s*\(\s*['"]([^'"]+)['"]""")
PLATFORMS = {"windows", "linux", "macos", "android", "ios"}
LEVELS = {"full", "partial", "none"}


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def ok(msg: str) -> int:
    print(f"OK {msg}")
    return 0


def check_identifier(name: str) -> tuple[bool, str]:
    if not name:
        return False, "identifier vide (attendu [a-z0-9-], ex sqlite, sqlite-store)"
    if "_" in name or any(c.isupper() for c in name):
        return False, (
            f"identifier invalide {name!r} : underscores/majuscules interdits "
            "(identifiers can only include lowercase ASCII, hyphens ...)"
        )
    if name.count(":") > 1 or "::" in name:
        return False, f"identifier invalide {name!r} : un seul ':' avec préfixe (ex plugin:perm)"
    if ":" in name:
        left, right = name.split(":")
        if not left or not right:
            return False, f"identifier invalide {name!r} : préfixe et nom requis autour de ':'"
        if len(name) > 129:
            return False, f"identifier invalide {name!r} : >129 caractères avec préfixe (max 129)"
        for part in (left, right):
            if len(part) > 64:
                return False, f"identifier invalide {name!r} : partie >64 caractères"
            if not BASE_RE.match(part):
                return False, (
                    f"identifier invalide {name!r} : partie {part!r} doit suivre "
                    "[a-z0-9-], tirets ni leading ni trailing"
                )
        return True, f"identifier {name!r} valide (préfixé)"
    if len(name) > 64:
        return False, f"identifier invalide {name!r} : >64 caractères (max 64)"
    if not BASE_RE.match(name):
        return False, (
            f"identifier invalide {name!r} : [a-z0-9-] seuls, tirets ni leading "
            "ni trailing (identifiers can only include lowercase ASCII ...)"
        )
    return True, f"identifier {name!r} valide"


def check_permission(path: pathlib.Path) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    try:
        data = tomllib.loads(raw)
    except Exception as e:
        print(f"FAIL {path}")
        print(f" - TOML illisible ({e})")
        return 1
    errors: list[str] = []
    info: list[str] = []
    if '"$schema"' not in raw and "'$schema'" not in raw and "$schema" not in data:
        errors.append('"$schema" = "schemas/schema.json" manquant (permissions/*.toml doc)')
    elif isinstance(data.get("$schema"), str) and "schemas/schema.json" not in data["$schema"]:
        errors.append('"$schema" doit pointer schemas/schema.json (permissions/*.toml doc)')
    perms = data.get("permission", [])
    if isinstance(perms, dict):
        perms = [perms]
    sets = data.get("set", [])
    if isinstance(sets, dict):
        sets = [sets]
    default = data.get("default")
    if not perms and not sets and default is None:
        errors.append("aucun [[permission]] / [[set]] / [default] (permissions/*.toml doc)")
    for i, perm in enumerate(perms):
        if not isinstance(perm, dict):
            errors.append(f"[[permission]] #{i} illisible (dict attendu)")
            continue
        ident = perm.get("identifier")
        if not isinstance(ident, str) or not ident:
            errors.append(f"[[permission]] #{i} sans identifier (permissions/*.toml doc)")
        else:
            valid, msg = check_identifier(ident)
            if not valid:
                errors.append(f"[[permission]] identifier {msg}")
        allowed_keys = {"identifier", "description", "commands", "scope"}
        for k in perm.keys():
            if k not in allowed_keys:
                errors.append(f"[[permission]] {ident!r} : clé inventée {k!r} (attendues: {sorted(allowed_keys)})")
        cmds = perm.get("commands", {})
        if cmds:
            if not isinstance(cmds, dict):
                errors.append(f"[[permission]] {ident!r} : commands doit être une table allow/deny")
            else:
                for side in ("allow", "deny"):
                    if side in cmds:
                        vals = cmds[side]
                        if not isinstance(vals, list) or not vals:
                            errors.append(f"commands.{side} de {ident!r} doit être une liste non vide")
                        else:
                            for c in vals:
                                if not isinstance(c, str) or not CMD_RE.match(c):
                                    errors.append(
                                        f"command inventée {c!r} dans commands.{side} de {ident!r} "
                                        "(snake_case, ex start_server, upload)"
                                    )
                for k in cmds.keys():
                    if k not in ("allow", "deny"):
                        errors.append(f"commands.{k} inventé pour {ident!r} (allow/deny seuls)")
        scope = perm.get("scope", {})
        if scope:
            if not isinstance(scope, dict):
                errors.append(f"scope de {ident!r} doit être une table allow/deny")
            else:
                for k in scope.keys():
                    if k not in ("allow", "deny"):
                        errors.append(f"scope.{k} inventé pour {ident!r} (allow/deny seuls)")
                # valeurs : liste de tables ou table unique ; on accepte sans valider le contenu métier
                if not scope:
                    errors.append(f"scope vide pour {ident!r}")
    for i, s in enumerate(sets):
        if not isinstance(s, dict):
            errors.append(f"[[set]] #{i} illisible")
            continue
        ident = s.get("identifier")
        if not isinstance(ident, str) or not ident:
            errors.append(f"[[set]] #{i} sans identifier")
        else:
            valid, msg = check_identifier(ident)
            if not valid:
                errors.append(f"[[set]] identifier {msg}")
        plist = s.get("permissions")
        if not isinstance(plist, list) or not plist:
            errors.append(f"[[set]] {ident!r} sans permissions = [...] (permissions/websocket.toml doc)")
        else:
            for p in plist:
                if not isinstance(p, str):
                    errors.append(f"[[set]] {ident!r} : permission non-string {p!r}")
                    continue
                valid, msg = check_identifier(p)
                if not valid:
                    errors.append(f"[[set]] {ident!r} référence {msg}")
        if "description" not in s:
            info.append(f"[[set]] {ident!r} sans description (recommandée doc)")
    if default is not None:
        if not isinstance(default, dict):
            errors.append("[default] illisible (table attendue)")
        else:
            plist = default.get("permissions")
            if not isinstance(plist, list) or not plist:
                errors.append("[default] sans permissions = [...] (permissions/default.toml doc)")
            else:
                for p in plist:
                    if not isinstance(p, str):
                        errors.append(f"[default] permission non-string {p!r}")
                        continue
                    valid, msg = check_identifier(p)
                    if not valid:
                        errors.append(f"[default] référence {msg}")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    detail = f"{len(perms)} permission(s), {len(sets)} set(s){', default' if default is not None else ''}"
    print(f"OK {path}: permissions fidèles ({detail})")
    for i in info:
        print(f" - {i}")
    return 0


def check_cargo(path: pathlib.Path) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    try:
        data = tomllib.loads(raw)
    except Exception as e:
        print(f"FAIL {path}")
        print(f" - TOML illisible ({e})")
        return 1
    errors: list[str] = []
    try:
        support = data["package"]["metadata"]["platforms"]["support"]
    except KeyError:
        print(f"FAIL {path}")
        print(" - missing [package.metadata.platforms.support] (develop/Plugins/index.mdx doc)")
        return 1
    if not isinstance(support, dict) or not support:
        print(f"FAIL {path}")
        print(" - [package.metadata.platforms.support] vide (windows/linux/macos/android/ios)")
        return 1
    for plat, val in support.items():
        if plat not in PLATFORMS:
            errors.append(f"plateforme inventée {plat!r} (attendues: {sorted(PLATFORMS)})")
            continue
        if not isinstance(val, dict):
            errors.append(f"{plat} doit être une table {{ level, notes? }}")
            continue
        level = val.get("level")
        if level not in LEVELS:
            errors.append(f"{plat}.level inventé {level!r} (attendus: {sorted(LEVELS)})")
        notes = val.get("notes")
        if notes is not None and not isinstance(notes, str):
            errors.append(f"{plat}.notes doit être une string Markdown (support table doc)")
        for k in val.keys():
            if k not in ("level", "notes"):
                errors.append(f"{plat}.{k} inventé (level/notes seuls)")
    name = data.get("package", {}).get("name", "")
    if isinstance(name, str) and name.startswith("tauri-plugin-"):
        suffix = name[len("tauri-plugin-"):]
        valid, msg = check_identifier(suffix)
        if not valid:
            errors.append(f"[package] name {msg} (préfixe tauri-plugin- + nom doc)")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    plats = ", ".join(f"{k}={v.get('level')}" for k, v in support.items())
    return ok(f"{path}: platforms.support fidèle ({plats})")


def check_invoke(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors: list[str] = []
    info: list[str] = []
    found_plugin = False
    for m in PLUGIN_INVOKE_RE.finditer(text):
        found_plugin = True
        pname, cmd = m.group(1), m.group(2)
        valid, msg = check_identifier(pname)
        if not valid:
            errors.append(f"invoke plugin {msg}")
        if not MOBILE_CMD_RE.match(cmd) and not CMD_RE.match(cmd):
            errors.append(f"commande invoke inventée {cmd!r} après plugin:{pname}| (ex upload, openCamera)")
        else:
            info.append(f"invoke plugin:{pname}|{cmd}")
    for m in BUILDER_RE.finditer(text):
        found_plugin = True
        pname = m.group(1)
        # <plugin-name> placeholder du guide : accepter comme gabarit doc
        if pname == "<plugin-name>":
            info.append('Builder::new("<plugin-name>") (placeholder doc)')
            continue
        valid, msg = check_identifier(pname)
        if not valid:
            errors.append(f"Builder {msg}")
        else:
            info.append(f'Builder::new("{pname}")')
    for m in RUN_MOBILE_RE.finditer(text):
        found_plugin = True
        cmd = m.group(1)
        if not MOBILE_CMD_RE.match(cmd) and not CMD_RE.match(cmd):
            errors.append(f"run_mobile_plugin commande inventée {cmd!r} (ex openCamera)")
        else:
            info.append(f'run_mobile_plugin("{cmd}")')
    for m in LISTENER_RE.finditer(text):
        found_plugin = True
        pname, evt = m.group(1), m.group(2)
        if pname == "<plugin-name>":
            info.append("addPluginListener('<plugin-name>', ...) (placeholder doc)")
        else:
            valid, msg = check_identifier(pname)
            if not valid:
                errors.append(f"addPluginListener plugin {msg}")
            else:
                info.append(f"addPluginListener('{pname}', '{evt}')")
        if not evt.strip():
            errors.append("addPluginListener event vide")
    if KOTLIN_PLUGIN_RE.search(text):
        found_plugin = True
        info.append("@TauriPlugin (Android, develop-mobile.mdx)")
        cmds = list(KOTLIN_CMD_RE.finditer(text))
        for m in cmds:
            info.append(f"@Command {m.group(1)}")
        if "@Command" not in text:
            errors.append("@TauriPlugin sans @Command (chaque @Command appelable Rust/JS, develop-mobile.mdx)")
        if "invoke.resolve" not in text and "invoke.reject" not in text:
            errors.append("@Command sans invoke.resolve/reject (develop-mobile.mdx)")
    for m in SWIFT_CMD_RE.finditer(text):
        found_plugin = True
        info.append(f"@objc {m.group(1)}(_ invoke: Invoke) (iOS, develop-mobile.mdx)")
    for m in TRIGGER_RE.finditer(text):
        info.append(f"trigger(\"{m.group(1)}\")")
    # invoke JS sans préfixe plugin: dans un fichier qui importe invoke -> KO
    if "invoke(" in text and "@tauri-apps/api/core" in text and not found_plugin:
        for m in BARE_INVOKE_RE.finditer(text):
            arg = m.group(1)
            if not arg.startswith("plugin:"):
                errors.append(
                    f"invoke('{arg}') sans préfixe plugin: (attendu invoke('plugin:<nom>|<cmd>'), "
                    "commands.rs + webview-src/index.ts doc)"
                )
                break
    if not found_plugin:
        # fichier Rust pur avec commandes mais sans Builder ? exiger au moins une ref plugin
        if "tauri::command" in text or "#[command]" in text:
            errors.append("commande Rust sans Builder::new ni invoke_handler (lib.rs doc, exposer via invoke_handler)")
        else:
            errors.append(
                "aucune référence plugin (invoke plugin:<nom>|, Builder::new, "
                "run_mobile_plugin ou addPluginListener attendus)"
            )
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"OK {path}: invoke plugin fidèle")
    for i in sorted(set(info))[:10]:
        print(f" - {i}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--identifier", help="nom de plugin / permission à valider")
    g.add_argument("--permission", help="fichier TOML permissions/*.toml à valider")
    g.add_argument("--cargo", help="Cargo.toml (platforms.support) à valider")
    g.add_argument("--invoke", help="fichier JS/TS/RS/KT/SWIFT avec invoke plugin à valider")
    args = ap.parse_args()
    if args.identifier is not None:
        valid, msg = check_identifier(args.identifier)
        if valid:
            return ok(msg + " (develop/Plugins/index.mdx)")
        print("FAIL --identifier")
        print(f" - {msg}")
        return 1
    if args.permission:
        return check_permission(pathlib.Path(args.permission))
    if args.cargo:
        return check_cargo(pathlib.Path(args.cargo))
    if args.invoke:
        return check_invoke(pathlib.Path(args.invoke))
    return 1


if __name__ == "__main__":
    sys.exit(main())
