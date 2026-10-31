#!/usr/bin/env python3
"""Check déterministe UI recettes Tauri v2 (seam basse tauri-ui-recettes).

Valide le comportement externe de l'agent sur des artefacts reproductibles
fidèles à la doc locale commit ec113a50 (EN canonique seule), sans inventer
de config ni d'API. Ne prouve PAS à lui seul la couverture doc : les pointeurs
source se vérifient dans la réponse.

Règles issues de tauri-docs/learn :
- windows : labels uniques non vides (app.windows|windows|tauri.windows),
  visible/decorations bool si présent, splashscreen exige main visible false
  (learn/splashscreen.mdx), url string si présente.
- fileAssociations : bundle.fileAssociations liste non vide, ext sans point,
  mimeType avec '/', role/rank enums Apple, androidIntentActionFilters subset
  Send/SendMultiple/View, exportedType identifier reverse-DNS
  (learn/mobile-file-associations.mdx).
- frontend : TrayIcon.new/Menu.new/Submenu.new/MenuItem/Check/Icon/Predefined,
  WebviewWindow, getCurrentWindow, defaultWindowIcon, setAsAppMenu,
  menuOnLeftClick, supportsMultipleWindows, invoke opened_urls + listen opened
  (cold+warm) ; Menu sans await using ni .close() = leak (learn/window-menu.mdx) ;
  TrayIcon.create/Menu.create inventés rejetés.
- rust : TrayIconBuilder/MenuBuilder/Menu::with_items/MenuItem::with_id,
  on_menu_event/on_tray_icon_event, get_webview_window + close/show,
  WebviewWindowBuilder + activity_name, RunEvent::Opened exige emit("opened"),
  SceneRequested exige WebviewWindowBuilder, TitleBarStyle ; WindowBuilder nu
  et TrayBuilder inventés rejetés.

Usage :
  python3 scripts/check-ui-recettes.py --config tauri.conf.json
  python3 scripts/check-ui-recettes.py --frontend menu.js
  python3 scripts/check-ui-recettes.py --rust splashscreen.rs
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROLE_ALLOWED = {"Editor", "Viewer", "Shell", "QLGenerator", "None"}
RANK_ALLOWED = {"Default", "Owner", "Alternate", "None"}
INTENT_ACTIONS_ALLOWED = {"Send", "SendMultiple", "View"}

FRONT_APIS = [
    "TrayIcon.new",
    "Menu.new",
    "Submenu.new",
    "MenuItem.new",
    "CheckMenuItem.new",
    "PredefinedMenuItem.new",
    "IconMenuItem.new",
    "WebviewWindow",
    "getCurrentWindow",
    "defaultWindowIcon",
    "setAsAppMenu",
    "menuOnLeftClick",
    "supportsMultipleWindows",
    "activityName",
    "opened_urls",
]

RUST_APIS = [
    "TrayIconBuilder",
    "MenuBuilder",
    "Menu::with_items",
    "MenuItem::with_id",
    "on_menu_event",
    "on_tray_icon_event",
    "get_webview_window",
    "WebviewWindowBuilder",
    "RunEvent::Opened",
    "RunEvent::SceneRequested",
    "activity_name",
    'emit("opened"',
    "emit('opened'",
    "OpenedUrls",
    "opened_urls",
    "TitleBarStyle",
    "show_menu_on_left_click",
]


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def find_windows(data: dict) -> list | None:
    if isinstance(data.get("app"), dict) and isinstance(data["app"].get("windows"), list):
        return data["app"]["windows"]
    if isinstance(data.get("windows"), list):
        return data["windows"]
    if isinstance(data.get("tauri"), dict) and isinstance(data["tauri"].get("windows"), list):
        return data["tauri"]["windows"]
    return None


def check_config(path: pathlib.Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"{path}: JSON illisible ({e})")
    errors: list[str] = []
    info: list[str] = []
    windows = find_windows(data)
    bundle = data.get("bundle") if isinstance(data.get("bundle"), dict) else {}
    file_assocs = bundle.get("fileAssociations") if isinstance(bundle, dict) else None
    if windows is None and file_assocs is None:
        return fail(f"{path}: ni windows (app.windows) ni bundle.fileAssociations (learn/splashscreen.mdx, learn/mobile-file-associations.mdx)")
    if windows is not None:
        if not isinstance(windows, list) or not windows:
            errors.append("windows doit être une liste non vide (learn/splashscreen.mdx)")
        else:
            labels: list[str] = []
            for i, w in enumerate(windows):
                if not isinstance(w, dict):
                    errors.append(f"windows[{i}] doit être un objet")
                    continue
                label = w.get("label", "")
                if not isinstance(label, str) or not label.strip():
                    # splashscreen.mdx omet le label main dans un extrait ; on tolère
                    # l'absence seulement si une seule fenêtre sans label ? Non : label requis.
                    # Pour compat doc simplifiée {"windows":[{"label":"main"...}]}, exiger label.
                    errors.append(f"windows[{i}].label manquant ou vide (labels uniques exigés)")
                    continue
                if re.search(r"\s|/", label):
                    errors.append(f"windows[{i}].label invalide: {label!r} (sans espace ni slash)")
                labels.append(label)
                for k in ("visible", "decorations", "transparent", "focus", "resizable"):
                    if k in w and not isinstance(w[k], bool):
                        errors.append(f"windows[{i}].{k} doit être booléen (learn/window-customization.mdx)")
                if "url" in w and (not isinstance(w["url"], str) or not w["url"].strip()):
                    errors.append(f"windows[{i}].url doit être une chaîne non vide")
            dupes = sorted({x for x in labels if labels.count(x) > 1})
            if dupes:
                errors.append(f"windows labels doivent être uniques (doublons: {', '.join(dupes)})")
            low = [x.lower() for x in labels]
            if any("splashscreen" in x for x in low):
                mains = [w for w in windows if isinstance(w, dict) and str(w.get("label", "")).lower() == "main"]
                if not mains:
                    errors.append("splashscreen exige une fenêtre label 'main' (learn/splashscreen.mdx)")
                else:
                    m = mains[0]
                    if m.get("visible", True) is not False:
                        errors.append("splashscreen exige main avec visible false (learn/splashscreen.mdx)")
            info.append(f"windows: {labels}")
    if file_assocs is not None:
        if not isinstance(file_assocs, list) or not file_assocs:
            errors.append("bundle.fileAssociations doit être une liste non vide")
        else:
            for i, e in enumerate(file_assocs):
                if not isinstance(e, dict):
                    errors.append(f"fileAssociations[{i}] doit être un objet")
                    continue
                ext = e.get("ext")
                if not isinstance(ext, list) or not ext or not all(isinstance(x, str) and x.strip() for x in ext):
                    errors.append(f"fileAssociations[{i}].ext doit être une liste non vide de strings")
                else:
                    for x in ext:
                        if x.startswith("."):
                            errors.append(f"fileAssociations[{i}].ext {x!r} sans point initial (doc : without leading dot)")
                        if re.search(r"\s", x):
                            errors.append(f"fileAssociations[{i}].ext {x!r} invalide")
                mime = e.get("mimeType")
                if mime is not None and (not isinstance(mime, str) or "/" not in mime):
                    errors.append(f"fileAssociations[{i}].mimeType doit contenir '/' (ex image/png)")
                role = e.get("role")
                if role is not None and role not in ROLE_ALLOWED:
                    errors.append(f"fileAssociations[{i}].role inventé: {role!r} (Editor/Viewer/Shell/QLGenerator/None)")
                rank = e.get("rank")
                if rank is not None and rank not in RANK_ALLOWED:
                    errors.append(f"fileAssociations[{i}].rank inventé: {rank!r} (Default/Owner/Alternate/None)")
                acts = e.get("androidIntentActionFilters")
                if acts is not None:
                    if not isinstance(acts, list) or not acts or any(a not in INTENT_ACTIONS_ALLOWED for a in acts):
                        errors.append(
                            f"fileAssociations[{i}].androidIntentActionFilters inventé: {acts!r} (Send/SendMultiple/View seuls)"
                        )
                exp_type = e.get("exportedType")
                if exp_type is not None:
                    if not isinstance(exp_type, dict):
                        errors.append(f"fileAssociations[{i}].exportedType doit être un objet")
                    else:
                        ident = exp_type.get("identifier", "")
                        if not isinstance(ident, str) or "." not in ident:
                            errors.append(f"fileAssociations[{i}].exportedType.identifier doit être reverse-DNS (ex com.example.myapp.mydata)")
                        conforms = exp_type.get("conformsTo")
                        if conforms is not None and (not isinstance(conforms, list) or not conforms):
                            errors.append(f"fileAssociations[{i}].exportedType.conformsTo doit être une liste non vide")
            info.append(f"fileAssociations: {len(file_assocs)} entrée(s)")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        for i in info:
            print(f"   {i}")
        return 1
    print(f"OK {path}")
    for i in info:
        print(f" - {i}")
    return 0


def check_frontend(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors: list[str] = []
    info: list[str] = []
    if "TrayIcon.create" in text or "Menu.create" in text:
        errors.append("API inventée: TrayIcon.create/Menu.create — doc : TrayIcon.new/Menu.new (learn/system-tray.mdx, learn/window-menu.mdx)")
    has_api = any(a in text for a in FRONT_APIS)
    if not has_api:
        errors.append("aucune API UI doc détectée (TrayIcon.new/Menu.new/WebviewWindow/getCurrentWindow/listen/invoke opened attendus)")
    has_menu_new = any(
        x in text
        for x in ("Menu.new", "Submenu.new", "MenuItem.new", "CheckMenuItem.new", "PredefinedMenuItem.new", "IconMenuItem.new")
    )
    if has_menu_new and "await using" not in text and ".close()" not in text:
        errors.append("menu leak: Menu/Submenu/MenuItem sans 'await using' ni .close() (learn/window-menu.mdx § Prevent JavaScript menu leaks)")
    has_listen_opened = bool(re.search(r"listen\s*\(\s*['\"]opened['\"]", text))
    has_invoke_opened = "opened_urls" in text
    if has_listen_opened ^ has_invoke_opened:
        # xor : un seul des deux = pattern cold/warm incomplet
        errors.append("pattern file-open incomplet: invoke('opened_urls') (cold) + listen('opened') (warm) exigés ensemble (learn/mobile-file-associations.mdx)")
    if "WebviewWindow" in text and "new WebviewWindow" not in text and "WebviewWindowBuilder" not in text:
        info.append("note: WebviewWindow importé sans construction visible")
    else:
        found = sorted({a for a in FRONT_APIS if a in text})
        if found:
            info.append(f"frontend APIs: {', '.join(found)}")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        for i in info:
            print(f"   {i}")
        return 1
    print(f"OK {path}")
    for i in info:
        print(f" - {i}")
    return 0


def check_rust(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors: list[str] = []
    info: list[str] = []
    if re.search(r"\bTrayBuilder\b", text):
        errors.append("API inventée: TrayBuilder — doc : TrayIconBuilder (learn/system-tray.mdx)")
    if re.search(r"(?<![A-Za-z:])WindowBuilder::", text):
        errors.append("API inventée: WindowBuilder — doc : WebviewWindowBuilder (learn/mobile-multiwindow.mdx, learn/splashscreen.mdx)")
    if re.search(r"(?<!show_)menu_on_left_click", text):
        errors.append("API inventée: menu_on_left_click — doc : show_menu_on_left_click (learn/system-tray.mdx)")
    has_api = any(a in text for a in RUST_APIS)
    if not has_api:
        errors.append("aucune API UI Rust doc détectée (TrayIconBuilder/MenuBuilder/get_webview_window/WebviewWindowBuilder/RunEvent attendus)")
    if "RunEvent::Opened" in text and not re.search(r'\.emit\s*\(\s*"opened"', text) and not re.search(r"\.emit\s*\(\s*'opened'", text):
        errors.append('RunEvent::Opened sans emit("opened") : la livraison warm exige app.emit("opened", urls) (learn/mobile-file-associations.mdx)')
    if "RunEvent::SceneRequested" in text and "WebviewWindowBuilder" not in text:
        errors.append("SceneRequested sans WebviewWindowBuilder : créer la fenêtre main-N via WebviewWindowBuilder (learn/mobile-multiwindow.mdx)")
    found = sorted({a for a in RUST_APIS if a in text})
    if found:
        info.append(f"rust APIs: {', '.join(found)}")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        for i in info:
            print(f"   {i}")
        return 1
    print(f"OK {path}")
    for i in info:
        print(f" - {i}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None)
    ap.add_argument("--frontend", default=None)
    ap.add_argument("--rust", default=None)
    args = ap.parse_args()
    if not args.config and not args.frontend and not args.rust:
        print("FAIL: fournir --config et/ou --frontend et/ou --rust")
        return 2
    code = 0
    if args.config:
        r = check_config(pathlib.Path(args.config))
        code = code or r
    if args.frontend:
        r = check_frontend(pathlib.Path(args.frontend))
        code = code or r
    if args.rust:
        r = check_rust(pathlib.Path(args.rust))
        code = code or r
    return code


if __name__ == "__main__":
    sys.exit(main())
