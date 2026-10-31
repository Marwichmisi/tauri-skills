"""Seam basse tauri-frontend-bindings : check des appels JS/TS vs signatures documentées.

Règles issues des sources régénérées au commit figé :
- tauri@37b3be6 packages/api/src (core, event, mocks, app, path, window...)
- plugins-workspace@df59420 plugins/*/guest-js (27 modules)
- API Rust linkée docs.rs, jamais copiée.

Le check valide le comportement externe de l'agent (imports et appels JS
fidèles à la doc), jamais les détails internes du skill.
"""
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-frontend-bindings.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *args], capture_output=True, text=True
    )
    return r


def test_exemple_invoke_ok_passe():
    ok = EXAMPLES / "invoke-channel.js"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--frontend", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_event_ok_passe():
    ok = EXAMPLES / "event-listen.js"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--frontend", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_plugin_ok_passe():
    ok = EXAMPLES / "plugin-dialog-fs.js"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--frontend", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_mocks_ok_passe():
    ok = EXAMPLES / "mocks.js"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--frontend", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_import_invente_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "import { fooBarBaz } from '@tauri-apps/api/fake-module';\n"
        "import { open } from '@tauri-apps/plugin-fake';\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "import" in (r.stdout + r.stderr).lower()


def test_event_nom_invalide_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "import { emit } from '@tauri-apps/api/event';\n"
        "await emit('bad event!');\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "event" in (r.stdout + r.stderr).lower()


def test_invoke_sans_module_echoue(tmp_path):
    bad = tmp_path / "bad.js"
    bad.write_text(
        "await invoke('greet', { name: 'tauri' });\n",
        encoding="utf-8",
    )
    r = run("--frontend", str(bad))
    assert r.returncode != 0
    assert "invoke" in (r.stdout + r.stderr).lower()


def test_rust_sans_docsrs_echoue(tmp_path):
    bad = tmp_path / "bad.rs"
    bad.write_text(
        "#[tauri::command]\nasync fn download(url: String) -> Result<()> { Ok(()) }\n",
        encoding="utf-8",
    )
    r = run("--rust", str(bad))
    assert r.returncode != 0
    assert "docs.rs" in (r.stdout + r.stderr).lower()


def test_rust_avec_docsrs_ok():
    ok = EXAMPLES / "channel-rust.rs"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--rust", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
