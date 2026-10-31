#!/usr/bin/env python3
"""Check déterministe de migration Tauri v1→v2 / bêta→stable (seam basse tauri-migrate).

Valide le comportement externe de l'agent sur les artefacts migrés, sans
inventer de valeurs. Ne prouve PAS à lui seul le chemin pas-à-pas : l'ordre
lire-le-guide → commande `migrate` → reprises manuelles se vérifie dans les
expectations d'eval (contenu réponse), pas ici.

Règles issues de tauri-docs commit ec113a50 (EN canonique seule) :
- tauri.conf : `package` supprimé (productName/version/mainBinaryName top-level),
  `tauri` renommé `app`, allowlist supprimée (-> capabilities/), distDir->frontendDist,
  devPath->devUrl, withGlobalTauri -> app.withGlobalTauri, updater -> plugins.updater
  (+ bundle.createUpdaterArtifacts requis, v1Compatible si app déjà distribuée),
  systemTray -> app.trayIcon, pattern -> app.security.pattern, bundle -> top-level,
  cli -> plugins.cli, fileDropEnabled -> app.windows dragDropEnabled.
- Cargo : bloc [lib] staticlib+cdylib+rlib exigé en mobile (main.rs -> lib.rs run()),
  tauri/tauri-build en version 2, features supprimées rejetées, plugins en version 2.
- JS : `@tauri-apps/api/tauri` -> `@tauri-apps/api/core`,
  `@tauri-apps/api/window` -> `@tauri-apps/api/webviewWindow`,
  modules api/* -> `@tauri-apps/plugin-*` (^2.0.0), onMenuClicked supprimé.
- Rust : `tauri::api::*`, fs_scope, get_cli_matches, Menu/SystemTray, get_window
  rejetés (voir references/from-v1-code.md pour le remplacement exact).
- Bêta : permissions core sans préfixe `core:` rejetées (path:default -> core:path:default,
  ou core:default) ; vite `TAURI_ENV_PLATFORM`+internal-ip rejetés (-> TAURI_DEV_HOST).
- Env : anciennes variables rejetées (voir OLD_ENV) ; deps npm/cargo syncées
  (même mineure api/tauri, versions exactes plugin npm == cargo).

Usage :
  python3 scripts/check-migrate.py --tauri-conf <conf> [--cargo-toml <f> [--mobile]]
    [--package-json <f>] [--js-entry <f>] [--rust-src <f>] [--capability <f>]
    [--vite-config <f>] [--text-file <f>]
"""
import argparse
import json
import pathlib
import re
import sys

REMOVED_FEATURES = [
    "reqwest-client",
    "reqwest-native-tls-vendored",
    "process-command-api",
    "shell-open-api",
    "windows7-compat",
    "linux-protocol-headers",
]

# system-tray et updater retirés en tant que features ; tray-icon est le nouveau nom.
REMOVED_FEATURES_EXACT = {"system-tray", "updater"}

OLD_JS_MODULES = [
    "api/tauri",
    "api/cli",
    "api/clipboard",
    "api/dialog",
    "api/fs",
    "api/global-shortcut",
    "api/http",
    "api/notification",
    "api/os",
    "api/process",
    "api/shell",
    "api/updater",
    "api/window",
]

# Remplacement documenté par module v1 (from-tauri-1.mdx) ; défaut générique
# `@tauri-apps/plugin-<nom>`. Cas particulier doc : le JS utilise
# `@tauri-apps/plugin-clipboard-manager` alors que le Rust utilise
# `tauri_plugin_clipboard` (même fichier, § Migrate to Clipboard Plugin).
JS_REPLACEMENTS = {
    "api/tauri": "@tauri-apps/api/core (tauri->core)",
    "api/window": "@tauri-apps/api/webviewWindow (window renommé)",
    "api/clipboard": "@tauri-apps/plugin-clipboard-manager (^2.0.0)",
}

BARE_CORE_PERMS = {
    "path:default",
    "event:default",
    "window:default",
    "app:default",
    "image:default",
    "resources:default",
    "menu:default",
    "tray:default",
}

OLD_ENV = [
    ("TAURI_PRIVATE_KEY", "TAURI_SIGNING_PRIVATE_KEY"),
    ("TAURI_KEY_PASSWORD", "TAURI_SIGNING_PRIVATE_KEY_PASSWORD"),
    ("TAURI_SKIP_DEVSERVER_CHECK", "TAURI_CLI_NO_DEV_SERVER_WAIT"),
    ("TAURI_DEV_SERVER_PORT", "TAURI_CLI_PORT"),
    ("TAURI_PATH_DEPTH", "TAURI_CLI_CONFIG_DEPTH"),
    ("TAURI_FIPS_COMPLIANT", "TAURI_BUNDLER_WIX_FIPS_COMPLIANT"),
    ("TAURI_DEV_WATCHER_IGNORE_FILE", "TAURI_CLI_WATCHER_IGNORE_FILENAME"),
    ("TAURI_TRAY", "TAURI_LINUX_AYATANA_APPINDICATOR"),
    ("TAURI_APPLE_DEVELOPMENT_TEAM", "APPLE_DEVELOPMENT_TEAM"),
    ("TAURI_PLATFORM", "TAURI_ENV_PLATFORM"),
    ("TAURI_ARCH", "TAURI_ENV_ARCH"),
    ("TAURI_FAMILY", "TAURI_ENV_FAMILY"),
    ("TAURI_PLATFORM_VERSION", "TAURI_ENV_PLATFORM_VERSION"),
    ("TAURI_PLATFORM_TYPE", "TAURI_ENV_PLATFORM_TYPE"),
    ("TAURI_DEBUG", "TAURI_ENV_DEBUG"),
]


def check_conf(path, errors):
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{path}: JSON illisible ({e})")
        return
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    if "package" in data:
        errors.append(
            f"{path}: 'package' v1 présent (productName/version -> top-level, "
            "ajouter mainBinaryName, voir references/from-v1-config.md)"
        )
    if "tauri" in data:
        errors.append(
            f"{path}: clé 'tauri' v1 présente (renommée 'app', voir references/from-v1-config.md)"
        )
    if "allowlist" in raw:
        errors.append(
            f"{path}: 'allowlist' v1 présent (supprimé -> capabilities/, voir Migrate Permissions)"
        )
    build = data.get("build") or {}
    if "distDir" in build:
        errors.append(f"{path}: 'build.distDir' v1 (renommé 'frontendDist')")
    if "devPath" in build:
        errors.append(f"{path}: 'build.devPath' v1 (renommé 'devUrl')")
    if "withGlobalTauri" in build:
        errors.append(
            f"{path}: 'build.withGlobalTauri' v1 (déplacé 'app.withGlobalTauri')"
        )
    if "app" not in data:
        errors.append(f"{path}: missing 'app' (clé 'tauri' renommée 'app' en v2)")
    if not build.get("frontendDist"):
        errors.append(f"{path}: missing 'build.frontendDist' (ex ../dist, renommé de distDir)")
    if not build.get("devUrl"):
        errors.append(f"{path}: missing 'build.devUrl' (ex http://localhost:5173)")
    if "fileDropEnabled" in raw:
        errors.append(
            f"{path}: 'fileDropEnabled' v1 (renommé 'dragDropEnabled' sous app.windows)"
        )
    if "systemTray" in raw:
        errors.append(f"{path}: 'systemTray' v1 (renommé 'app.trayIcon')")
    if "assetScope" in raw and "assetProtocol" not in raw:
        errors.append(
            f"{path}: 'assetScope' v1 sans 'assetProtocol' "
            "(déplacé app > security > assetProtocol > scope, voir security/asset-protocol/)"
        )
    plugins = data.get("plugins") or {}
    bundle = data.get("bundle") or {}
    if "updater" in plugins and "createUpdaterArtifacts" not in bundle:
        errors.append(
            f"{path}: plugins.updater sans bundle.createUpdaterArtifacts "
            "(requis en v2, 'v1Compatible' si app v1 déjà distribuée)"
        )


def check_cargo(path, errors, mobile):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(r'tauri\s*=\s*[{"][^}\n]*version\s*=\s*"(\d+)', text)
    m2 = re.search(r'^tauri\s*=\s*"(\d+)', text, re.M)
    ver = (m.group(1) if m else (m2.group(1) if m2 else None))
    if ver is None:
        errors.append(f"{path}: dépendance 'tauri' introuvable (attendu version \"2\")")
    elif not ver.startswith("2"):
        errors.append(
            f"{path}: tauri version {ver} (attendu 2.x, voir references/updating-dependencies.md)"
        )
    for feat in REMOVED_FEATURES:
        if feat in text:
            errors.append(
                f"{path}: feature Cargo supprimée '{feat}' "
                "(voir Removed Cargo Features, utiliser le plugin shell/updater/notification)"
            )
    for feat in sorted(REMOVED_FEATURES_EXACT):
        if re.search(rf'"{feat}"|\b{re.escape(feat)}\b.*=.*\[', text) or (
            feat in text and "features" in text
        ):
            # vérification stricte : feature listée dans features = [...]
            if re.search(r"features\s*=\s*\[[^\]]*" + re.escape(feat), text):
                errors.append(
                    f"{path}: feature Cargo supprimée '{feat}' "
                    "(updater->plugin, system-tray->tray-icon)"
                )
    if mobile:
        if "[lib]" not in text:
            errors.append(
                f"{path}: bloc [lib] manquant (mobile exige staticlib+cdylib+rlib, "
                "main.rs -> lib.rs run(), voir references/from-v1-code.md)"
            )
        elif not all(k in text for k in ("staticlib", "cdylib", "rlib")):
            errors.append(
                f"{path}: crate-type incomplet (attendu [\"staticlib\", \"cdylib\", \"rlib\"])"
            )


def check_package(path, errors):
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{path}: JSON illisible ({e})")
        return
    deps = {}
    deps.update(data.get("dependencies") or {})
    deps.update(data.get("devDependencies") or {})
    for name in ("@tauri-apps/api", "@tauri-apps/cli"):
        if name in deps and "2" not in str(deps[name]):
            errors.append(
                f"{path}: {name} en version {deps[name]!r} (attendu 2.x, "
                "voir references/updating-dependencies.md)"
            )
    for name, ver in deps.items():
        if name.startswith("@tauri-apps/plugin-") and str(ver).strip().startswith("1"):
            errors.append(f"{path}: {name} en version 1.x (attendu ^2.0.0)")


def check_js(path, errors):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    for mod in OLD_JS_MODULES:
        # borne stricte : évite que 'api/cli' matche 'api/clipboard'
        if re.search(r"@tauri-apps/" + re.escape(mod) + r"(?![a-zA-Z0-9_-])", text):
            hint = JS_REPLACEMENTS.get(mod, f"@tauri-apps/plugin-{mod.split('/')[-1]} (^2.0.0)")
            errors.append(
                f"{path}: import v1 '@tauri-apps/{mod}' (remplacé par {hint}, "
                "voir references/from-v1-code.md)"
            )
    if "tauri-plugin-" in text and "-api" in text and "git" in text:
        errors.append(
            f"{path}: plugin v1 via git 'tauri-plugin-*-api' "
            "(v2 publiés @tauri-apps/plugin-<nom>, voir references/from-v1-code.md)"
        )
    if "onMenuClicked" in text:
        errors.append(
            f"{path}: 'onMenuClicked' supprimé (intercepter les événements menu à la création, "
            "voir Migrate to new Window API)"
        )
    check_old_env(path, text, errors)


def check_rust(path, errors):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    for pat, hint in [
        ("tauri::api::", "module api supprimé -> plugin dédié (dialog/fs/http/shell/...)"),
        ("fs_scope", "Manager::fs_scope supprimé -> tauri_plugin_fs::FsExt"),
        ("get_cli_matches", "App::get_cli_matches supprimé -> tauri-plugin-cli"),
        ("SystemTray", "SystemTray supprimé -> tauri::tray::TrayIconBuilder"),
        ("get_window", "get_window renommé get_webview_window"),
        ("WindowBuilder", "WindowBuilder renommé WebviewWindowBuilder"),
        ("WindowUrl", "WindowUrl renommé WebviewUrl"),
        ("api::process::Command", "api::process supprimé -> tauri_plugin_shell + CommandEvent"),
    ]:
        if pat in text:
            errors.append(f"{path}: motif Rust v1 '{pat}' ({hint})")


def check_capability(path, errors):
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{path}: JSON illisible ({e})")
        return
    perms = data.get("permissions") or []
    for p in perms:
        if p in BARE_CORE_PERMS:
            errors.append(
                f"{path}: permission bêta '{p}' sans préfixe 'core:' "
                f"(attendu 'core:{p}' ou 'core:default', voir references/from-beta.md)"
            )
    if not data.get("identifier"):
        errors.append(f"{path}: missing 'identifier'")
    if not data.get("windows") and not data.get("webviews"):
        errors.append(f"{path}: missing 'windows' ou 'webviews'")


def check_vite(path, errors):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    if "TAURI_ENV_PLATFORM" in text and "android|ios" in text:
        errors.append(
            f"{path}: détection mobile bêta via TAURI_ENV_PLATFORM "
            "(remplacée par process.env.TAURI_DEV_HOST, voir references/from-beta.md)"
        )
    if "internal-ip" in text or "internalIpV4Sync" in text:
        errors.append(
            f"{path}: paquet 'internal-ip' bêta (inutile, utiliser TAURI_DEV_HOST directement)"
        )
    if "TAURI_DEV_HOST" not in text:
        errors.append(
            f"{path}: 'TAURI_DEV_HOST' absent (requis en stable pour le dev server, "
            "voir references/from-beta.md)"
        )
    check_old_env(path, text, errors)


def check_old_env(path, text, errors):
    for old, new in OLD_ENV:
        # \b suffit : '_' est un caractère de mot, donc 'TAURI_PLATFORM'
        # ne matche jamais à l'intérieur de 'TAURI_ENV_PLATFORM'.
        if re.search(r"\b" + re.escape(old) + r"\b", text) and new not in text:
            errors.append(
                f"{path}: env var v1 '{old}' (renommée '{new}', voir references/from-v1-config.md)"
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tauri-conf", default=None)
    ap.add_argument("--cargo-toml", default=None)
    ap.add_argument("--mobile", action="store_true")
    ap.add_argument("--package-json", default=None)
    ap.add_argument("--js-entry", default=None)
    ap.add_argument("--rust-src", default=None)
    ap.add_argument("--capability", default=None)
    ap.add_argument("--vite-config", default=None)
    ap.add_argument("--text-file", default=None)
    args = ap.parse_args()

    if not any(
        [
            args.tauri_conf,
            args.cargo_toml,
            args.package_json,
            args.js_entry,
            args.rust_src,
            args.capability,
            args.vite_config,
            args.text_file,
        ]
    ):
        print("FAIL: aucun fichier fourni (voir --help)")
        return 2

    errors: list[str] = []
    if args.tauri_conf:
        check_conf(args.tauri_conf, errors)
    if args.cargo_toml:
        check_cargo(args.cargo_toml, errors, args.mobile)
    if args.package_json:
        check_package(args.package_json, errors)
    if args.js_entry:
        check_js(args.js_entry, errors)
    if args.rust_src:
        check_rust(args.rust_src, errors)
        check_old_env(
            args.rust_src, pathlib.Path(args.rust_src).read_text(encoding="utf-8"), errors
        )
    if args.capability:
        check_capability(args.capability, errors)
    if args.vite_config:
        check_vite(args.vite_config, errors)
    if args.text_file:
        text = pathlib.Path(args.text_file).read_text(encoding="utf-8")
        check_old_env(args.text_file, text, errors)

    if errors:
        print("FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print("OK migration: artefacts conformes v2/stable (voir references/)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
