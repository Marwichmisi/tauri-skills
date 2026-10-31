"""Seam basse tauri-migrate : check déterministe de migration v1→v2 / bêta→stable.

Vérifie le comportement externe de l'agent avec le skill (artefacts fidèles
à la doc), jamais les détails internes du skill.

Référence : ticket #9, gabarit docs/gabarit-skill.md, étalon repris du
pilote skills/tauri-security-capabilities/scripts/check-capabilities.py
et de skills/tauri-start/scripts/check-start.py.

Couvre (doc locale commit ec113a50, EN canonique) :
- tauri.conf.json v2 (clés renommées, allowlist supprimée, updater/callout)
- Cargo.toml (lib mobile, tauri v2, features supprimées)
- JS/Rust (imports core/plugins, window→webviewWindow, TAURI_DEV_HOST)
- capabilities (préfixe core: bêta→stable)
- env vars renommées, deps npm/cargo syncées (rappelées, vérifiées ici par grep)
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-migrate.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )
    return r


def test_exemple_conf_v2_ok():
    conf = EXAMPLES / "tauri.conf.v2.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run("--tauri-conf", conf)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_conf_v1_rejetee_package_tauri_distdir():
    bad = EXAMPLES / "tauri.conf.v1.json"
    assert bad.exists(), f"manquant: {bad}"
    r = run("--tauri-conf", bad)
    assert r.returncode != 0, f"FAIL attendu:\n{r.stdout}\n{r.stderr}"
    out = (r.stdout + r.stderr).lower()
    assert "package" in out or "tauri" in out or "distdir" in out


def test_updater_sans_artifacts_echoue(tmp_path):
    conf = {
        "productName": "x",
        "version": "0.1.0",
        "app": {"withGlobalTauri": True},
        "build": {
            "frontendDist": "../dist",
            "devUrl": "http://localhost:5173",
        },
        "plugins": {"updater": {"active": True}},
        "bundle": {},
    }
    p = tmp_path / "tauri.conf.json"
    p.write_text(json.dumps(conf), encoding="utf-8")
    r = run("--tauri-conf", p)
    assert r.returncode != 0
    assert "createupdaterartifacts" in (r.stdout + r.stderr).lower()


def test_cargo_mobile_lib_ok():
    cargo = EXAMPLES / "Cargo.v2-mobile.toml"
    assert cargo.exists(), f"manquant: {cargo}"
    r = run("--cargo-toml", cargo, "--mobile")
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_cargo_sans_lib_mobile_echoue(tmp_path):
    p = tmp_path / "Cargo.toml"
    p.write_text('[package]\nname = "x"\n[dependencies]\ntauri = "2"\n', encoding="utf-8")
    r = run("--cargo-toml", p, "--mobile")
    assert r.returncode != 0
    assert "lib" in (r.stdout + r.stderr).lower()


def test_cargo_feature_supprimee_echoue(tmp_path):
    p = tmp_path / "Cargo.toml"
    p.write_text(
        '[dependencies]\ntauri = { version = "2", features = ["process-command-api"] }\n',
        encoding="utf-8",
    )
    r = run("--cargo-toml", p)
    assert r.returncode != 0
    assert "process-command-api" in (r.stdout + r.stderr)


def test_js_v1_imports_rejetes():
    bad = EXAMPLES / "main.v1.js"
    assert bad.exists(), f"manquant: {bad}"
    r = run("--js-entry", bad)
    assert r.returncode != 0, f"FAIL attendu:\n{r.stdout}\n{r.stderr}"
    assert "core" in (r.stdout + r.stderr).lower() or "plugin" in (
        r.stdout + r.stderr
    ).lower()


def test_js_v2_ok():
    good = EXAMPLES / "main.v2.js"
    assert good.exists(), f"manquant: {good}"
    r = run("--js-entry", good)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_capability_bare_prefix_echoue():
    bad = EXAMPLES / "capability-beta.json"
    assert bad.exists(), f"manquant: {bad}"
    r = run("--capability", bad)
    assert r.returncode != 0, f"FAIL attendu:\n{r.stdout}\n{r.stderr}"
    assert "core:" in (r.stdout + r.stderr)


def test_capability_core_ok():
    good = EXAMPLES / "capability-stable.json"
    assert good.exists(), f"manquant: {good}"
    r = run("--capability", good)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_vite_beta_rejete_platform(tmp_path):
    bad = EXAMPLES / "vite.config.beta.js"
    assert bad.exists(), f"manquant: {bad}"
    r = run("--vite-config", bad)
    assert r.returncode != 0, f"FAIL attendu:\n{r.stdout}\n{r.stderr}"
    assert "tauri_dev_host" in (r.stdout + r.stderr).lower()


def test_vite_stable_ok():
    good = EXAMPLES / "vite.config.stable.js"
    assert good.exists(), f"manquant: {good}"
    r = run("--vite-config", good)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_old_env_var_rejetee(tmp_path):
    p = tmp_path / "deploy.sh"
    p.write_text('export TAURI_PRIVATE_KEY="x"\n', encoding="utf-8")
    r = run("--text-file", p)
    assert r.returncode != 0
    assert "tauri_signing_private_key" in (r.stdout + r.stderr).lower()


def test_js_clipboard_hint_nomme_clipboard_manager(tmp_path):
    # Doc from-tauri-1 § Migrate to Clipboard Plugin : JS = plugin-clipboard-manager.
    p = tmp_path / "a.js"
    p.write_text(
        'import { readText } from "@tauri-apps/api/clipboard";\n', encoding="utf-8"
    )
    r = run("--js-entry", p)
    assert r.returncode != 0
    assert "plugin-clipboard-manager" in (r.stdout + r.stderr)


def test_new_env_platform_ne_declenche_pas(tmp_path):
    # TAURI_ENV_PLATFORM est la forme v2 : ne doit pas être signalée comme v1.
    p = tmp_path / "vite.config.js"
    p.write_text(
        "const t = process.env.TAURI_ENV_PLATFORM;\nconst h = process.env.TAURI_DEV_HOST;\n",
        encoding="utf-8",
    )
    r = run("--text-file", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
