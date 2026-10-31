"""Seam basse tauri-config-cli-reference : check déterministe config/CLI/env.

Vérifie le comportement externe de l'agent (spec #6, ticket #17) :
- --config valide un tauri.conf.json avec plugins.cli in-app sans inventer de schéma
- --cli distingue la CLI dev (tauri dev/build/ios) de l'usage in-app (getMatches/CliExt)
- --env n'accepte que les variables documentées dans environment-variables.mdx
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-config-cli.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *args], capture_output=True, text=True
    )
    return r


def test_exemple_config_ok():
    p = EXAMPLES / "tauri.conf.cli.json"
    assert p.exists(), f"manquant: {p}"
    r = run("--config", str(p))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_config_cli_hors_plugins_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps({"cli": {"description": "x"}}),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "plugins.cli" in (r.stdout + r.stderr)


def test_config_arg_sans_name_echoue(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "plugins": {
                    "cli": {
                        "description": "x",
                        "args": [{"short": "v", "description": "sans nom"}],
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    r = run("--config", str(bad))
    assert r.returncode != 0
    assert "name" in (r.stdout + r.stderr).lower()


def test_exemple_cli_ok():
    p = EXAMPLES / "cli-commands.sh"
    assert p.exists(), f"manquant: {p}"
    r = run("--cli", str(p))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_cli_tauri_cli_commande_inexistante_echoue(tmp_path):
    bad = tmp_path / "bad.sh"
    bad.write_text("pnpm tauri cli --help\n", encoding="utf-8")
    r = run("--cli", str(bad))
    assert r.returncode != 0
    assert "cli" in (r.stdout + r.stderr).lower()


def test_exemple_env_ok():
    p = EXAMPLES / "env.sh"
    assert p.exists(), f"manquant: {p}"
    r = run("--env", str(p))
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_env_variable_inventee_echoue(tmp_path):
    bad = tmp_path / "bad.env"
    bad.write_text("TAURI_FAKE_INVENTED=1\n", encoding="utf-8")
    r = run("--env", str(bad))
    assert r.returncode != 0
    assert "TAURI_FAKE_INVENTED" in (r.stdout + r.stderr)
