"""Seam basse tauri-distribution : check déterministe updater/bundle/sign.

Comportement externe vérifié (spec #6, ticket #14) :
- valide la config updater de tauri.conf.json (pubkey, endpoints https, createUpdaterArtifacts)
- valide les bundle targets documentés (pas de skill par OS)
- valide les noms de variables de signature documentées (pas d'invention)
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-distribution.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *args], capture_output=True, text=True
    )
    return r


def test_exemple_updater_ok_passe():
    ok = EXAMPLES / "tauri.conf.updater.json"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--updater", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_updater_sans_pubkey_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "bundle": {"createUpdaterArtifacts": True},
                "plugins": {"updater": {"endpoints": ["https://example.com/x"]}},
            }
        ),
        encoding="utf-8",
    )
    r = run("--updater", str(bad))
    assert r.returncode != 0
    assert "pubkey" in (r.stdout + r.stderr).lower()


def test_updater_endpoint_non_https_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "bundle": {"createUpdaterArtifacts": True},
                "plugins": {
                    "updater": {
                        "pubkey": "dW50cnVzdCB0ZXN0a2V5",
                        "endpoints": ["http://insecure.example.com/x"],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    r = run("--updater", str(bad))
    assert r.returncode != 0
    assert "https" in (r.stdout + r.stderr).lower()


def test_updater_pubkey_chemin_fichier_rejete(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "bundle": {"createUpdaterArtifacts": True},
                "plugins": {
                    "updater": {
                        "pubkey": "./publickey.pem",
                        "endpoints": ["https://example.com/x"],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    r = run("--updater", str(bad))
    assert r.returncode != 0
    assert "pubkey" in (r.stdout + r.stderr).lower()


def test_bundle_targets_documentes_ok():
    ok = EXAMPLES / "tauri.conf.bundle.json"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--bundle", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_bundle_target_invente_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"bundle": {"targets": ["exe"]}}),
        encoding="utf-8",
    )
    r = run("--bundle", str(bad))
    assert r.returncode != 0
    assert "target" in (r.stdout + r.stderr).lower() or "bundle" in (
        r.stdout + r.stderr
    ).lower()


def test_sign_vars_documentees_ok():
    ok = EXAMPLES / "signing.env"
    assert ok.exists(), f"manquant: {ok}"
    r = run("--sign", str(ok))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"


def test_sign_var_inventee_echoue(tmp_path):
    bad = tmp_path / "bad.env"
    bad.write_text("MY_SIGN_KEY=foo\n", encoding="utf-8")
    r = run("--sign", str(bad))
    assert r.returncode != 0
