"""Seam basse tauri-ipc-bridge : check déterministe de l'échange Rust ↔ frontend.

Vérifie le comportement externe de l'agent avec le skill (patterns fidèles
à la doc), jamais les détails internes du skill.

Référence : ticket #11, gabarit docs/gabarit-skill.md, étalon repris du
pilote skills/tauri-security-capabilities/scripts/check-capabilities.py.

Couvre :
- Rust : #[tauri::command], unicité, enregistrement invoke_handler/generate_handler,
  interdiction `pub fn` dans lib.rs (limitation glue code doc)
- Frontend : invoke/emit/listen/Channel/sidecar, appariement avec une commande
  Rust ou un event Rust (échange complet)
- Config : bundle.externalBin (liste non vide) + cohérence sidecar Rust/JS,
  bundle.resources (liste ou map non vide)
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-ipc-bridge.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )
    return r


def test_exemple_command_pair_ok_passe():
    rust = EXAMPLES / "command-rust.rs"
    front = EXAMPLES / "command-frontend.js"
    assert rust.exists(), f"manquant: {rust}"
    assert front.exists(), f"manquant: {front}"
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_event_pair_ok_passe():
    rust = EXAMPLES / "event-rust.rs"
    front = EXAMPLES / "event-frontend.js"
    assert rust.exists(), f"manquant: {rust}"
    assert front.exists(), f"manquant: {front}"
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_sidecar_config_ok_passe():
    conf = EXAMPLES / "tauri.conf.sidecar.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run("--config", conf)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_resources_config_ok_passe():
    conf = EXAMPLES / "tauri.conf.resources.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run("--config", conf)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_command_sans_handler_echoue(tmp_path):
    rust = tmp_path / "lib.rs"
    rust.write_text(
        '#[tauri::command]\nfn my_custom_command() {}\n',
        encoding="utf-8",
    )
    front = tmp_path / "app.js"
    front.write_text(
        "import { invoke } from '@tauri-apps/api/core';\ninvoke('my_custom_command');\n",
        encoding="utf-8",
    )
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode != 0
    assert "handler" in (r.stdout + r.stderr).lower()


def test_invoke_sans_command_rust_echoue(tmp_path):
    rust = tmp_path / "lib.rs"
    rust.write_text(
        '#[tauri::command]\nfn my_custom_command() {}\n'
        'tauri::Builder::default().invoke_handler(tauri::generate_handler![my_custom_command]);\n',
        encoding="utf-8",
    )
    front = tmp_path / "app.js"
    front.write_text(
        "import { invoke } from '@tauri-apps/api/core';\ninvoke('commande_inventee');\n",
        encoding="utf-8",
    )
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode != 0
    assert "invoke" in (r.stdout + r.stderr).lower()


def test_pub_dans_lib_interdit_echoue(tmp_path):
    rust = tmp_path / "lib.rs"
    rust.write_text(
        '#[tauri::command]\npub fn my_custom_command() {}\n'
        'tauri::Builder::default().invoke_handler(tauri::generate_handler![my_custom_command]);\n',
        encoding="utf-8",
    )
    front = tmp_path / "app.js"
    front.write_text(
        "import { invoke } from '@tauri-apps/api/core';\ninvoke('my_custom_command');\n",
        encoding="utf-8",
    )
    # Copie vers un fichier nommé lib.rs : le check refuse pub dans lib.rs
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode != 0
    assert "pub" in (r.stdout + r.stderr).lower()


def test_command_dupliquee_echoue(tmp_path):
    rust = tmp_path / "cmds.rs"
    rust.write_text(
        '#[tauri::command]\nfn dup() {}\n#[tauri::command]\nfn dup() {}\n'
        'tauri::Builder::default().invoke_handler(tauri::generate_handler![dup]);\n',
        encoding="utf-8",
    )
    front = tmp_path / "app.js"
    front.write_text(
        "import { invoke } from '@tauri-apps/api/core';\ninvoke('dup');\n",
        encoding="utf-8",
    )
    r = run("--rust", rust, "--frontend", front)
    assert r.returncode != 0
    assert "unique" in (r.stdout + r.stderr).lower()


def test_sidecar_js_hors_externalbin_echoue(tmp_path):
    conf = tmp_path / "tauri.conf.json"
    conf.write_text(
        json.dumps({"bundle": {"externalBin": ["binaries/my-sidecar"]}}),
        encoding="utf-8",
    )
    front = tmp_path / "app.js"
    front.write_text(
        "import { Command } from '@tauri-apps/plugin-shell';\n"
        "const c = Command.sidecar('binaries/autre-binaire');\n",
        encoding="utf-8",
    )
    r = run("--frontend", front, "--config", conf)
    assert r.returncode != 0
    assert "sidecar" in (r.stdout + r.stderr).lower()


def test_triple_dans_externalbin_echoue(tmp_path):
    conf = tmp_path / "tauri.conf.json"
    conf.write_text(
        json.dumps(
            {"bundle": {"externalBin": ["binaries/my-sidecar-x86_64-unknown-linux-gnu"]}}
        ),
        encoding="utf-8",
    )
    r = run("--config", conf)
    assert r.returncode != 0
    assert "triple" in (r.stdout + r.stderr).lower()
