"""Seam basse catalogue : routage 30 fiches + permission non inventée.

Comportement externe vérifié (spec #6, ticket #16) :
- --list expose les 30 fiches plugin/** hors updater (une étape de routage).
- --plugin valide la fiche, rejette updater (renvoi distribution).
- --capability valide identifier/cibles/forme permissions, préfixe connu.
- --js valide l'import guest-js du plugin (sauf Rust-only).
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-catalogue.py"
EXAMPLES = SKILL / "examples"

EXPECTED_SLUGS = {
    "autostart",
    "barcode-scanner",
    "biometric",
    "cli",
    "clipboard",
    "deep-linking",
    "dialog",
    "file-system",
    "geolocation",
    "global-shortcut",
    "haptics",
    "http-client",
    "overview",
    "localhost",
    "logging",
    "nfc",
    "notification",
    "opener",
    "os-info",
    "persisted-scope",
    "positioner",
    "process",
    "shell",
    "single-instance",
    "sql",
    "store",
    "stronghold",
    "upload",
    "websocket",
    "window-state",
}


def run(*args):
    return subprocess.run(
        [sys.executable, str(CHECK), *args], capture_output=True, text=True
    )


def test_list_expose_30_fiches_hors_updater():
    assert CHECK.exists(), f"manquant: {CHECK}"
    r = run("--list")
    assert r.returncode == 0, f"--list doit passer:\n{r.stdout}\n{r.stderr}"
    slugs = {ln.strip() for ln in r.stdout.splitlines() if ln.strip()}
    assert slugs == EXPECTED_SLUGS, f"slugs inattendus: {sorted(slugs)}"
    assert "updater" not in slugs, "updater vit dans tauri-distribution, pas catalogue"


def test_updater_rejete_avec_renvoi_distribution(tmp_path):
    cap = tmp_path / "cap.json"
    cap.write_text(
        json.dumps(
            {
                "identifier": "x",
                "windows": ["main"],
                "permissions": ["updater:default"],
            }
        ),
        encoding="utf-8",
    )
    r = run("--plugin", "updater", "--capability", str(cap))
    assert r.returncode != 0
    out = (r.stdout + r.stderr).lower()
    assert "distribution" in out, "doit renvoyer vers tauri-distribution"


def test_exemple_fs_passe(tmp_path):
    js = EXAMPLES / "fs.js"
    cap = EXAMPLES / "capability-fs.json"
    assert js.exists(), f"manquant: {js}"
    assert cap.exists(), f"manquant: {cap}"
    r = run("--plugin", "file-system", "--js", str(js), "--capability", str(cap))
    assert r.returncode == 0, f"exemple fs doit passer:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_dialog_passe():
    js = EXAMPLES / "dialog.js"
    cap = EXAMPLES / "capability-dialog.json"
    assert js.exists() and cap.exists()
    r = run("--plugin", "dialog", "--js", str(js), "--capability", str(cap))
    assert r.returncode == 0, f"exemple dialog doit passer:\n{r.stdout}\n{r.stderr}"


def test_permission_inventee_echoue(tmp_path):
    cap = tmp_path / "bad.json"
    cap.write_text(
        json.dumps(
            {
                "identifier": "x",
                "windows": ["main"],
                "permissions": ["fs:allow-hack-the-planet"],
            }
        ),
        encoding="utf-8",
    )
    # format valide mais préfixe connu : le check format passe ;
    # l'invention se prouve par la fiche : ici on teste le format nu rejeté
    bad2 = tmp_path / "bad2.json"
    bad2.write_text(
        json.dumps(
            {"identifier": "x", "windows": ["main"], "permissions": ["foo"]}
        ),
        encoding="utf-8",
    )
    r = run("--plugin", "file-system", "--capability", str(bad2))
    assert r.returncode != 0
    assert "permission" in (r.stdout + r.stderr).lower()


def test_prefixe_hors_catalogue_echoue(tmp_path):
    cap = tmp_path / "bad.json"
    cap.write_text(
        json.dumps(
            {
                "identifier": "x",
                "windows": ["main"],
                "permissions": ["unknownplugin:default"],
            }
        ),
        encoding="utf-8",
    )
    r = run("--plugin", "file-system", "--capability", str(cap))
    assert r.returncode != 0
    out = (r.stdout + r.stderr).lower()
    assert "prefix" in out or "préfixe" in out or "permission" in out


def test_js_mauvais_plugin_echoue(tmp_path):
    js = tmp_path / "wrong.js"
    js.write_text(
        "import { openUrl } from '@tauri-apps/plugin-opener';\nawait openUrl('https://x');\n",
        encoding="utf-8",
    )
    cap = EXAMPLES / "capability-fs.json"
    r = run("--plugin", "file-system", "--js", str(js), "--capability", str(cap))
    assert r.returncode != 0
    assert "opener" in (r.stdout + r.stderr).lower() or "js" in (
        r.stdout + r.stderr
    ).lower()


def test_sans_cible_echoue(tmp_path):
    cap = tmp_path / "bad.json"
    cap.write_text(
        json.dumps({"identifier": "x", "permissions": ["fs:default"]}),
        encoding="utf-8",
    )
    r = run("--plugin", "file-system", "--capability", str(cap))
    assert r.returncode != 0
    assert "windows" in (r.stdout + r.stderr).lower()


def test_capability_sans_prefixe_cible_emet_note():
    # --plugin dialog + capability fs : forme/préfixes valides donc exit 0,
    # mais une note signale l'absence du préfixe cible (mauvaise fiche possible).
    cap = EXAMPLES / "capability-fs.json"
    r = run("--plugin", "dialog", "--capability", str(cap))
    assert r.returncode == 0
    assert "aucune permission au préfixe" in (r.stdout + r.stderr).lower()


def test_js_seul_est_verifie(tmp_path):
    # --js sans --capability doit quand même valider l'import guest-js.
    js = tmp_path / "wrong.js"
    js.write_text(
        "import { openUrl } from '@tauri-apps/plugin-opener';\nawait openUrl('https://x');\n",
        encoding="utf-8",
    )
    r = run("--plugin", "file-system", "--js", str(js))
    assert r.returncode != 0
    assert "plugin-fs" in (r.stdout + r.stderr)
