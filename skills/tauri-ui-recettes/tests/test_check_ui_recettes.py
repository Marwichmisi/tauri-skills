"""Seam basse tauri-ui-recettes : check déterministe fenêtres/menus/tray/splashscreen/mobile.

Comportement externe vérifié (spec #6, ticket #15) :
- valide la config tauri.conf.json (windows labels uniques, splashscreen main hidden, fileAssociations doc seules)
- valide le frontend JS (TrayIcon.new/Menu.new await using, WebviewWindow, opened cold+warm)
- valide le Rust (TrayIconBuilder/MenuBuilder, on_menu_event, WebviewWindowBuilder, RunEvent::Opened emit, SceneRequested)
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-ui-recettes.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True, text=True,
    )
    return r


def test_exemple_windows_config_ok():
    conf = EXAMPLES / "tauri.conf.windows.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run("--config", str(conf))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_file_associations_config_ok():
    conf = EXAMPLES / "tauri.conf.file-associations.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run("--config", str(conf))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_menu_frontend_ok():
    f = EXAMPLES / "menu.js"
    assert f.exists(), f"manquant: {f}"
    r = run("--frontend", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_tray_frontend_ok():
    f = EXAMPLES / "tray.js"
    assert f.exists(), f"manquant: {f}"
    r = run("--frontend", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_exemple_titlebar_frontend_ok():
    f = EXAMPLES / "titlebar.js"
    assert f.exists(), f"manquant: {f}"
    r = run("--frontend", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_exemple_splashscreen_rust_ok():
    f = EXAMPLES / "splashscreen.rs"
    assert f.exists(), f"manquant: {f}"
    r = run("--rust", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_exemple_mobile_frontend_ok():
    f = EXAMPLES / "mobile-windows.js"
    assert f.exists(), f"manquant: {f}"
    r = run("--frontend", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_exemple_mobile_rust_ok():
    f = EXAMPLES / "mobile-windows.rs"
    assert f.exists(), f"manquant: {f}"
    r = run("--rust", str(f))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_windows_label_duplique_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"app": {"windows": [{"label": "main"}, {"label": "main"}]}}),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "label" in (r.stdout + r.stderr).lower() or "unique" in (r.stdout + r.stderr).lower()


def test_splashscreen_sans_main_hidden_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"app": {"windows": [{"label": "splashscreen", "url": "/splashscreen"}]}}),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "main" in (r.stdout + r.stderr).lower()


def test_file_association_ext_point_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"bundle": {"fileAssociations": [{"ext": [".png"], "mimeType": "image/png"}]}}),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "ext" in (r.stdout + r.stderr).lower()


def test_file_association_role_invente_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"bundle": {"fileAssociations": [{"ext": ["png"], "mimeType": "image/png", "role": "SuperEditor"}]}}),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "role" in (r.stdout + r.stderr).lower()


def test_menu_js_sans_await_using_ni_close_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "import { Menu } from '@tauri-apps/api/menu';\n"
        "const menu = await Menu.new({ items: [{ id: 'quit', text: 'Quit' }] });\n"
        "await menu.setAsAppMenu();\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "close" in (r.stdout + r.stderr).lower() or "leak" in (r.stdout + r.stderr).lower()


def test_tray_api_inventee_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "import { TrayIcon } from '@tauri-apps/api/tray';\n"
        "const tray = await TrayIcon.create({});\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "trayicon" in (r.stdout + r.stderr).lower() or "new" in (r.stdout + r.stderr).lower()


def test_opened_warm_sans_cold_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "import { listen } from '@tauri-apps/api/event';\n"
        "await listen('opened', (e) => {});\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "opened_urls" in (r.stdout + r.stderr).lower()


def test_rust_opened_sans_emit_echoue(tmp_path):
    bad = tmp_path / "bad.rs"
    bad.write_text(
        "if let tauri::RunEvent::Opened { urls } = event {}\n",
        encoding="utf-8",
    )
    r = run("--rust", str(bad))
    assert r.returncode != 0
    assert "emit" in (r.stdout + r.stderr).lower()


def test_rust_scene_sans_builder_echoue(tmp_path):
    bad = tmp_path / "bad.rs"
    bad.write_text(
        "if let tauri::RunEvent::SceneRequested { .. } = event {}\n",
        encoding="utf-8",
    )
    r = run("--rust", str(bad))
    assert r.returncode != 0
    assert "webviewwindowbuilder" in (r.stdout + r.stderr).lower() or "scene" in (r.stdout + r.stderr).lower()


def test_rust_builder_invente_echoue(tmp_path):
    bad = tmp_path / "bad.rs"
    bad.write_text(
        "let w = tauri::WindowBuilder::new(app, 'main').build().unwrap();\n",
        encoding="utf-8",
    )
    r = run("--rust", str(bad))
    assert r.returncode != 0


def test_rust_menu_on_left_click_invente_echoue(tmp_path):
    bad = tmp_path / "bad.rs"
    bad.write_text(
        "let t = TrayIconBuilder::new().menu_on_left_click(true).build(app)?;\n",
        encoding="utf-8",
    )
    r = run("--rust", str(bad))
    assert r.returncode != 0
    assert "show_menu_on_left_click" in (r.stdout + r.stderr).lower()
