"""Seam basse pilote : check déterministe d'une capability JSON.

Étalon repris du prototype throwaway (branch prototype/gabarit-skill,
prototypes/gabarit-tauri-security/scripts/check-capabilities.py) :
- valide identifier, cibles windows/webviews, forme des permissions
- cas OK et KO testés, aucune permission inventée.
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-capabilities.py"
EXAMPLES = SKILL / "examples"


def run(path):
    r = subprocess.run(
        [sys.executable, str(CHECK), str(path)], capture_output=True, text=True
    )
    return r


def test_exemple_ok_passe():
    ok = EXAMPLES / "default-capability.json"
    assert ok.exists(), f"manquant: {ok}"
    r = run(ok)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_sans_identifier_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"windows": ["main"], "permissions": ["core:window:default"]}),
        encoding="utf-8",
    )
    r = run(bad)
    assert r.returncode != 0
    assert "identifier" in (r.stdout + r.stderr).lower()


def test_sans_cible_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"identifier": "x", "permissions": ["core:window:default"]}),
        encoding="utf-8",
    )
    r = run(bad)
    assert r.returncode != 0
    assert "windows" in (r.stdout + r.stderr).lower()


def test_permission_inventee_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "identifier": "x",
                "windows": ["main"],
                "permissions": ["foo"],  # forme invalide, permission inventée
            }
        ),
        encoding="utf-8",
    )
    r = run(bad)
    assert r.returncode != 0
    assert "permission" in (r.stdout + r.stderr).lower()


def test_deny_et_allow_acceptes(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(
        json.dumps(
            {
                "identifier": "x",
                "windows": ["*"],
                "permissions": [
                    "core:window:allow-set-title",
                    "core:window:deny-set-title",
                    "fs:default",
                ],
            }
        ),
        encoding="utf-8",
    )
    r = run(good)
    assert r.returncode == 0, r.stdout + r.stderr
