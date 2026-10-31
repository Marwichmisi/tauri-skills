#!/usr/bin/env python3
"""Check déterministe debug et tests Tauri v2 (seam basse tauri-dev-quality).

Valide le comportement externe de l'agent sur des artefacts reproductibles
fidèles à la doc locale, sans inventer d'outillage. Ne prouve PAS à lui seul
la couverture doc : les pointeurs source (fichier + commit + titre) se
vérifient dans la réponse, exigés par les expectations d'eval.

Règles issues de tauri-docs commit ec113a50 (EN canonique seule) :
- mock  : imports @tauri-apps/api/mocks limités à mockIPC/mockWindows/
          clearMocks, clearMocks exigé, shouldMockEvents seulement avec mockIPC.
- wdio  : route service ('tauri' + appBinaryPath + driverProvider
          embedded/external/crabnebula) OU route manuelle (tauri-driver spawn
          + 'tauri:options' + application). Manuelle = Windows/Linux seuls.
- vscode: launch.json version 0.2.0, type lldb/cppvsdbg seul, cargo args avec
          --manifest-path=./src-tauri/Cargo.toml, --no-default-features en dev,
          preLaunchTask ui:dev/ui:build.
- ci    : cargo install tauri-driver + webkit2gtk-driver/xvfb (linux) ou
          msedgedriver-tool (windows) + xvfb-run yarn test.
- linux : vars documentées seules (WEBKIT_DISABLE_DMABUF_RENDERER,
          WEBKIT_DISABLE_COMPOSITING_MODE, __NV_DISABLE_EXPLICIT_SYNC,
          RUST_BACKTRACE), garde #[cfg(target_os = "linux")] exigée pour WEBKIT_*.

Usage :
  python3 scripts/check-dev-quality.py --mock examples/mock-ipc.js
  python3 scripts/check-dev-quality.py --wdio examples/wdio-service.conf.js
  python3 scripts/check-dev-quality.py --vscode examples/launch.json
  python3 scripts/check-dev-quality.py --ci examples/webdriver.yml
  python3 scripts/check-dev-quality.py --linux examples/linux-workaround.rs
"""
import argparse
import json
import pathlib
import re
import sys

MOCK_ALLOWED = {"mockIPC", "mockWindows", "clearMocks"}
WDIO_PROVIDERS = {"embedded", "external", "crabnebula"}
LINUX_ALLOWED = {
    "WEBKIT_DISABLE_DMABUF_RENDERER",
    "WEBKIT_DISABLE_COMPOSITING_MODE",
    "__NV_DISABLE_EXPLICIT_SYNC",
    "RUST_BACKTRACE",
}


def fail(msg):
    print(f"FAIL: {msg}")
    return 1


def ok(msg):
    print(f"OK {msg}")
    return 0


def check_mock(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors = []
    if "@tauri-apps/api/mocks" not in text:
        errors.append("import @tauri-apps/api/mocks manquant (mockIPC/mockWindows/clearMocks)")
    # imports depuis mocks limités à l'allowlist
    for m in re.finditer(r"import\s*\{([^}]*)\}\s*from\s*['\"]@tauri-apps/api/mocks['\"]", text):
        for name in [n.strip() for n in m.group(1).split(",") if n.strip()]:
            if name not in MOCK_ALLOWED:
                errors.append(f"mock API inventée: {name} (autorisés: {sorted(MOCK_ALLOWED)})")
    if "mockIPC" not in text and "mockWindows" not in text:
        errors.append("aucun appel mockIPC/mockWindows (mocking.mdx)")
    if "clearMocks" not in text:
        errors.append("clearMocks manquant (doc exige de clear après chaque run)")
    if "shouldMockEvents" in text and "mockIPC" not in text:
        errors.append("shouldMockEvents sans mockIPC (option de mockIPC, mocking.mdx)")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    return ok(f"{path}: mock fidèle (mocking.mdx)")


def check_wdio(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors = []
    is_service = bool(re.search(r"['\"]tauri['\"]\s*,", text) and "services" in text)
    has_binary = "appBinaryPath" in text
    has_options = "tauri:options" in text
    has_driver_spawn = "tauri-driver" in text
    has_application = "application" in text
    if not (is_service or has_options or has_driver_spawn):
        errors.append("ni service 'tauri' ni 'tauri:options' ni tauri-driver (webdriver/index.mdx)")
    if is_service:
        if not has_binary:
            errors.append("route service sans appBinaryPath (webdriver/index.mdx)")
        m = re.search(r"driverProvider\s*:\s*['\"]([^'\"]+)['\"]", text)
        if not m:
            # embedded est le défaut doc, toléré sans champ explicite
            pass
        elif m.group(1) not in WDIO_PROVIDERS:
            errors.append(f"driverProvider inventé: {m.group(1)} (attendus: {sorted(WDIO_PROVIDERS)})")
    if has_driver_spawn or has_options:
        # route manuelle : Windows/Linux seuls, binaire debug, host/port ou usingServer
        if not has_application:
            errors.append("route manuelle sans application (tauri:options.application)")
        if "127.0.0.1:4444" not in text and "usingServer" not in text and ("host" not in text or "port" not in text):
            errors.append("route manuelle sans host/port ou usingServer 127.0.0.1:4444")
    if not is_service and not has_driver_spawn and not has_options:
        errors.append("ni specs ni capabilities (config wdio incomplète)")
    elif has_driver_spawn and ("specs" not in text and "capabilities" not in text):
        errors.append("route manuelle sans specs ni capabilities (config wdio incomplète)")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    route = "service" if is_service and not has_driver_spawn else ("manuelle" if has_driver_spawn else "service")
    return ok(f"{path}: wdio route {route} fidèle")


def check_vscode(path: pathlib.Path) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    # launch.json doc contient des commentaires // (JSONC VS Code) : les retirer
    no_block = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    no_line = re.sub(r"(?m)^\s*//.*$", "", no_block)
    no_line = re.sub(r"(?m)(?<![\"':/])//.*$", "", no_line)
    try:
        data = json.loads(no_line)
    except Exception as e:
        return fail(f"{path}: JSON illisible ({e})")
    errors = []
    if data.get("version") != "0.2.0":
        errors.append("version 0.2.0 attendue (vscode.mdx)")
    configs = data.get("configurations")
    if not isinstance(configs, list) or not configs:
        errors.append("configurations manquantes")
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    for c in configs:
        t = c.get("type")
        if t not in ("lldb", "cppvsdbg"):
            errors.append(f"type inventé: {t!r} (attendus: lldb vscode-lldb, cppvsdbg Windows)")
        if c.get("request") != "launch":
            errors.append(f"request launch attendu (config {c.get('name')})")
        cargo = c.get("cargo", {})
        args = " ".join(cargo.get("args", [])) if isinstance(cargo.get("args"), list) else ""
        program = c.get("program", "")
        if "src-tauri/Cargo.toml" not in args and "src-tauri" not in program:
            errors.append(f"manifest-path src-tauri/Cargo.toml ou program src-tauri/target manquant ({c.get('name')})")
        if "preLaunchTask" not in c:
            errors.append(f"preLaunchTask manquant ({c.get('name')}: ui:dev/ui:build)")
    # dev doit couper les default-features (le CLI le fait, en direct il faut le passer)
    blob = json.dumps(data)
    if "build" in blob and "--no-default-features" not in blob and "--release" not in blob:
        errors.append("--no-default-features (dev) ou --release (prod) attendu dans cargo.args")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    return ok(f"{path}: launch.json fidèle ({len(configs)} configs)")


def check_ci(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors = []
    if "cargo install tauri-driver" not in text:
        errors.append("cargo install tauri-driver manquant (ci.md)")
    if "webkit2gtk-driver" not in text and "xvfb" not in text:
        errors.append("dépendances linux manquantes (webkit2gtk-driver/xvfb, ci.md)")
    if "msedgedriver-tool" not in text:
        errors.append("msedgedriver-tool manquant (windows, ci.md)")
    if "xvfb-run" not in text:
        errors.append("xvfb-run manquant (display Linux, ci.md)")
    if "yarn test" not in text and "npm test" not in text and "pnpm test" not in text:
        errors.append("commande test e2e-tests manquante (yarn test)")
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    return ok(f"{path}: CI webdriver fidèle")


def check_linux(path: pathlib.Path) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return fail(f"{path}: illisible ({e})")
    errors = []
    # vars set_var / = "1"
    found = re.findall(r'set_var\(\s*"([^"]+)"', text)
    found += [v for v in re.findall(r'"((?:WEBKIT|__NV|RUST)[A-Z_]*)"', text) if v not in found]
    if not found:
        errors.append("aucune var documentée (WEBKIT_DISABLE_DMABUF_RENDERER, ...)")
    for v in found:
        if v not in LINUX_ALLOWED:
            errors.append(f"var inventée: {v} (autorisées: {sorted(LINUX_ALLOWED)})")
    if any(v.startswith("WEBKIT_") for v in found) and 'target_os = "linux"' not in text:
        errors.append('garde #[cfg(target_os = "linux")] exigée pour WEBKIT_* (linux-graphics.md)')
    if errors:
        print(f"FAIL {path}")
        for e in errors:
            print(f" - {e}")
        return 1
    return ok(f"{path}: workaround linux fidèle ({', '.join(found)})")


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--mock", help="fichier JS de mock à valider")
    g.add_argument("--wdio", help="config wdio JS à valider")
    g.add_argument("--vscode", help="launch.json à valider")
    g.add_argument("--ci", help="workflow yml à valider")
    g.add_argument("--linux", help="snippet rs linux à valider")
    args = ap.parse_args()
    if args.mock:
        return check_mock(pathlib.Path(args.mock))
    if args.wdio:
        return check_wdio(pathlib.Path(args.wdio))
    if args.vscode:
        return check_vscode(pathlib.Path(args.vscode))
    if args.ci:
        return check_ci(pathlib.Path(args.ci))
    if args.linux:
        return check_linux(pathlib.Path(args.linux))
    return 1


if __name__ == "__main__":
    sys.exit(main())
