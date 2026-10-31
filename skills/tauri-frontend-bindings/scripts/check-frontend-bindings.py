#!/usr/bin/env python3
"""Check déterministe des appels JS/TS frontend Tauri v2 (seam basse tauri-frontend-bindings).

Sources régénérées avant écriture (commit figé tauri-docs ec113a50) :
- tauri@37b3be6 packages/api/src (core, event, mocks, app, path, window...)
- plugins-workspace@df59420 plugins/*/guest-js (27 modules)
- API Rust linkée docs.rs, jamais copiée.

Valide le comportement externe de l'agent (imports et appels JS fidèles
à la doc), jamais les détails internes du skill.

Usage :
  python3 scripts/check-frontend-bindings.py --frontend examples/invoke-channel.js
  python3 scripts/check-frontend-bindings.py --frontend examples/event-listen.js
  python3 scripts/check-frontend-bindings.py --rust examples/channel-rust.rs
  python3 scripts/check-frontend-bindings.py --frontend a.js --rust b.rs
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

CORE_MODULES = {
    "app", "core", "dpi", "event", "image", "menu", "mocks",
    "path", "tray", "webview", "webviewWindow", "window",
}

PLUGIN_MODULES = {
    "autostart", "barcode-scanner", "biometric", "cli",
    "clipboard-manager", "deep-link", "dialog", "fs",
    "geolocation", "global-shortcut", "haptics", "http",
    "log", "nfc", "notification", "opener", "os",
    "positioner", "process", "shell", "sql", "store",
    "stronghold", "updater", "upload", "websocket",
    "window-state",
}

IMPORT_RE = re.compile(
    r"""(?:from\s+['"]([^'"]+)['"]|import\s*\(\s*['"]([^'"]+)['"]\s*\))"""
)
INVOKE_RE = re.compile(r"""invoke\s*\(\s*['"]([^'"]*)['"]""")
LISTEN_RE = re.compile(r"""(?:listen|once|emit)\s*\(\s*['"]([^'"]+)['"]""")
EMITTO_RE = re.compile(
    r"""emitTo\s*\(\s*['"][^'"]+['"]\s*,\s*['"]([^'"]+)['"]"""
)
PLUGIN_INVOKE_RE = re.compile(r"""['"]plugin:([A-Za-z0-9_.\-]+)\|([A-Za-z0-9_\-]+)['"]""")
EVENT_OK_RE = re.compile(r"^(?:tauri://[A-Za-z0-9_\-/:]+|[A-Za-z0-9_\-/:]+)$")
DOCSRS_RE = re.compile(r"https://docs\.rs/tauri")
CHANNEL_RE = re.compile(r"new\s+Channel")
CONVERT_RE = re.compile(r"convertFileSrc\s*\(")
MOCK_RE = re.compile(r"\b(mockIPC|mockWindows|mockConvertFileSrc|clearMocks)\b")


def check_frontend(path: pathlib.Path):
    errors: list[str] = []
    info: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{path}: illisible ({e})"], []
    imports: list[str] = []
    for m in IMPORT_RE.finditer(text):
        imports.append(m.group(1) or m.group(2))
    core_imports: list[str] = []
    plugin_imports: list[str] = []
    for imp in imports:
        if imp == "@tauri-apps/api":
            core_imports.append("(bare)")
        elif imp.startswith("@tauri-apps/api/"):
            mod = imp[len("@tauri-apps/api/"):].split("/")[0]
            if mod in CORE_MODULES:
                core_imports.append(mod)
            else:
                errors.append(
                    f"import inconnu '{imp}' (module core attendu parmi {sorted(CORE_MODULES)})"
                )
        elif imp.startswith("@tauri-apps/plugin-"):
            name = imp[len("@tauri-apps/plugin-"):].split("/")[0]
            if name in PLUGIN_MODULES:
                plugin_imports.append(name)
            else:
                errors.append(
                    f"import inconnu '{imp}' (plugin attendu parmi 27 guest-js documentés)"
                )
        elif imp.startswith("tauri-plugin-") and imp.endswith("-api"):
            name = imp[len("tauri-plugin-"): -len("-api")]
            if name in PLUGIN_MODULES:
                plugin_imports.append(name + " (legacy)")
            else:
                errors.append(f"import legacy inconnu '{imp}'")
        elif imp.startswith("@tauri-apps/"):
            errors.append(f"import inconnu '{imp}' (ni @tauri-apps/api/* ni @tauri-apps/plugin-*)")
    if not core_imports and not plugin_imports:
        # Ne fail que si aucun import Tauri mais usage Tauri détecté,
        # ou si fichier censé démontrer les bindings sans import.
        if "invoke(" in text or "listen(" in text or "emit(" in text or "Channel" in text:
            errors.append(
                "invoke/listen/emit/Channel sans import documenté "
                "(@tauri-apps/api/core, @tauri-apps/api/event, ...)"
            )
        else:
            errors.append(
                "aucun import Tauri documenté "
                "(@tauri-apps/api/<module> ou @tauri-apps/plugin-<nom>)"
            )
    # invoke
    has_core = any(
        i == "@tauri-apps/api" or i.startswith("@tauri-apps/api/core")
        for i in imports
    )
    invokes = INVOKE_RE.findall(text)
    for cmd in invokes:
        if not cmd.strip():
            errors.append("invoke avec commande vide")
        if cmd.startswith("plugin:"):
            m = PLUGIN_INVOKE_RE.match(f"'{cmd}'")
            if not m:
                errors.append(
                    f"invoke plugin mal formé '{cmd}' "
                    "(attendu plugin:<nom>|<cmd>)"
                )
            elif m.group(1) not in PLUGIN_MODULES:
                errors.append(
                    f"invoke plugin inconnu '{cmd}' (plugin hors 27 guest-js)"
                )
    if invokes and not has_core:
        # invoke direct sans core, sauf si via wrapper plugin (plugin-* importé)
        if not plugin_imports:
            errors.append(
                "invoke sans import @tauri-apps/api/core "
                "(importer { invoke } from '@tauri-apps/api/core')"
            )
    # events
    for ev in LISTEN_RE.findall(text):
        if not EVENT_OK_RE.match(ev):
            errors.append(
                f"event name invalide '{ev}' "
                "(alphanum + -, /, :, _ ou tauri://...)"
            )
    for ev in EMITTO_RE.findall(text):
        if not EVENT_OK_RE.match(ev):
            errors.append(f"emitTo event invalide '{ev}'")
    # Channel
    if CHANNEL_RE.search(text) and not has_core:
        errors.append("new Channel sans import @tauri-apps/api/core")
    if CHANNEL_RE.search(text) and "onmessage" not in text:
        errors.append("Channel sans onmessage (assigner channel.onmessage avant invoke)")
    if CONVERT_RE.search(text) and not has_core:
        errors.append("convertFileSrc sans import @tauri-apps/api/core")
    # mocks
    if MOCK_RE.search(text):
        has_mocks = any("api/mocks" in i for i in imports)
        if not has_mocks:
            errors.append(
                "mockIPC/mockWindows/clearMocks sans import @tauri-apps/api/mocks"
            )
    # window.__TAURI__ : autorisé (withGlobalTauri), info seulement
    if "window.__TAURI__" in text:
        info.append("window.__TAURI__ détecté (requiert app.withGlobalTauri, voir tauri-start)")
    if core_imports:
        info.append(f"core imports: {sorted(set(core_imports))}")
    if plugin_imports:
        info.append(f"plugin imports: {sorted(set(plugin_imports))}")
    if invokes:
        info.append(f"invokes: {sorted(set(invokes)) or '—'}")
    return errors, info


def check_rust(path: pathlib.Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"{path}: illisible ({e})"], []
    errors: list[str] = []
    info: list[str] = []
    if not DOCSRS_RE.search(text):
        errors.append(
            "API Rust sans lien docs.rs (attendu https://docs.rs/tauri/... "
            "— API Rust linkée, jamais copiée)"
        )
    else:
        info.append("docs.rs link OK")
    if "tauri::ipc::Channel" in text:
        info.append("tauri::ipc::Channel détecté (pendant JS new Channel)")
    if "#[tauri::command]" in text:
        info.append("tauri::command détecté (implémentation côté Rust, appel via invoke)")
    return errors, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frontend", default=None)
    ap.add_argument("--rust", default=None)
    args = ap.parse_args()
    if not args.frontend and not args.rust:
        print("FAIL: fournir --frontend et/ou --rust")
        return 1
    errors: list[str] = []
    info: list[str] = []
    label_parts: list[str] = []
    if args.frontend:
        fp = pathlib.Path(args.frontend)
        e, i = check_frontend(fp)
        errors.extend(e)
        info.extend(i)
        label_parts.append(str(args.frontend))
    if args.rust:
        rp = pathlib.Path(args.rust)
        e, i = check_rust(rp)
        errors.extend(e)
        info.extend(i)
        label_parts.append(str(args.rust))
    label = " + ".join(label_parts)
    if errors:
        print(f"FAIL {label}")
        for e in errors:
            print(f" - {e}")
        for x in info:
            print(f"   {x}")
        return 1
    print(f"OK {label}")
    for x in info:
        print(f" - {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
