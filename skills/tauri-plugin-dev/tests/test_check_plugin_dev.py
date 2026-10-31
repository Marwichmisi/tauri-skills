"""Seam basse tauri-plugin-dev : check déterministe plugin desktop+mobile.

Vérifie le comportement externe de l'agent avec le skill (squelette fidèle
à la doc), jamais les détails internes du skill.

Référence : ticket #13, gabarit docs/gabarit-skill.md, étalon repris du
pilote skills/tauri-security-capabilities/scripts/check-capabilities.py.

Couvre (4 modes) :
- --identifier NAME : syntaxe identifiant doc (minuscules/chiffres/tirets,
  pas leading/trailing, un seul ':' avec préfixe, <=64 base / <=129 total).
- --permission FILE.toml : permission/set/default issus de develop/Plugins,
  $schema exigé, identifier valide, commands.allow/deny snake_case,
  scope allow/deny seuls, sets/default référencent des identifiers valides.
- --cargo FILE.toml : [package.metadata.platforms.support] avec plateformes
  documentées seules et level full/partial/none.
- --invoke FILE : guest-js/Rust avec plugin:<nom>|<commande>,
  Builder::new("<nom>"), run_mobile_plugin/addPluginListener ; aucun
  identifiant inventé.
"""
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-plugin-dev.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )
    return r


def test_exemple_permission_ok_passe():
    p = EXAMPLES / "permission-allow-start-server.toml"
    assert p.exists(), f"manquant: {p}"
    r = run("--permission", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_identifier_valides_passent():
    for name in ["sqlite", "sqlite-store", "my-plugin", "a"]:
        r = run("--identifier", name)
        assert r.returncode == 0, f"OK attendu pour {name}:\n{r.stdout}\n{r.stderr}"
    r = run("--identifier", "sqlite-store:allow-read")
    assert r.returncode == 0, f"OK attendu préfixé:\n{r.stdout}\n{r.stderr}"


def test_identifier_invalides_echouent(tmp_path):
    for bad in ["sqlite_store", "SqliteStore", "-sqlite", "sqlite-", "sqlite::store", ""]:
        r = run("--identifier", bad)
        assert r.returncode != 0, f"FAIL attendu pour {bad!r}"
        assert "identifier" in (r.stdout + r.stderr).lower()


def test_permission_sans_identifier_echoue(tmp_path):
    p = tmp_path / "bad.toml"
    p.write_text(
        '"$schema" = "schemas/schema.json"\n'
        '[[permission]]\n'
        'description = "sans identifier"\n',
        encoding="utf-8",
    )
    r = run("--permission", p)
    assert r.returncode != 0
    assert "identifier" in (r.stdout + r.stderr).lower()


def test_permission_commande_inventee_echoue(tmp_path):
    p = tmp_path / "bad.toml"
    p.write_text(
        '"$schema" = "schemas/schema.json"\n'
        '[[permission]]\n'
        'identifier = "allow-upload"\n'
        'description = "bad cmd"\n'
        'commands.allow = ["Bad Command!"]\n',
        encoding="utf-8",
    )
    r = run("--permission", p)
    assert r.returncode != 0
    assert "command" in (r.stdout + r.stderr).lower()


def test_exemple_cargo_ok_passe():
    p = EXAMPLES / "Cargo.plugin.toml"
    assert p.exists(), f"manquant: {p}"
    r = run("--cargo", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_cargo_level_invente_echoue(tmp_path):
    p = tmp_path / "Cargo.toml"
    p.write_text(
        '[package.metadata.platforms.support]\nwindows = { level = "total" }\n',
        encoding="utf-8",
    )
    r = run("--cargo", p)
    assert r.returncode != 0
    assert "level" in (r.stdout + r.stderr).lower()


def test_cargo_plateforme_inventee_echoue(tmp_path):
    p = tmp_path / "Cargo.toml"
    p.write_text(
        '[package.metadata.platforms.support]\nwindowsphone = { level = "full" }\n',
        encoding="utf-8",
    )
    r = run("--cargo", p)
    assert r.returncode != 0


def test_exemple_invoke_ok_passe():
    p = EXAMPLES / "guest-js-upload.js"
    assert p.exists(), f"manquant: {p}"
    r = run("--invoke", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemples_mobile_ok_passent():
    for name in ["mobile-command.kt", "mobile-command.swift", "mobile-invoke.rs", "plugin-listener.js"]:
        p = EXAMPLES / name
        assert p.exists(), f"manquant: {p}"
        r = run("--invoke", p)
        assert r.returncode == 0, f"OK attendu pour {name}:\n{r.stdout}\n{r.stderr}"
        assert "OK" in r.stdout


def test_invoke_sans_prefixe_plugin_echoue(tmp_path):
    p = tmp_path / "bad.js"
    p.write_text(
        "import { invoke } from '@tauri-apps/api/core'\n"
        "await invoke('upload', { url });\n",
        encoding="utf-8",
    )
    r = run("--invoke", p)
    assert r.returncode != 0
    assert "plugin" in (r.stdout + r.stderr).lower()
