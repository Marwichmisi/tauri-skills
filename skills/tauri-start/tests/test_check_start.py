"""Seam basse tauri-start : check déterministe de la config de démarrage.

Vérifie le comportement externe de l'agent avec le skill (config fidèle
à la doc), jamais les détails internes du skill.

Référence : ticket #8, gabarit docs/gabarit-skill.md, étalon repris du
pilote skills/tauri-security-capabilities/scripts/check-capabilities.py.

Couvre :
- tauri.conf.json build (frontendDist/devUrl/beforeDev/beforeBuild) par frontend
- valeurs documentées uniquement (aucune config inventée)
- structure projet requise (src-tauri/ layout)
"""
import json
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-start.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )
    return r


def write_conf(tmp_path, build, app=None):
    conf = {"build": build}
    if app is not None:
        conf["app"] = app
    p = tmp_path / "tauri.conf.json"
    p.write_text(json.dumps(conf), encoding="utf-8")
    return p


def test_exemple_vite_ok_passe():
    conf = EXAMPLES / "tauri.conf.vite.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run(conf, "--frontend", "vite")
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_nextjs_out_ok():
    conf = EXAMPLES / "tauri.conf.nextjs.json"
    assert conf.exists(), f"manquant: {conf}"
    r = run(conf, "--frontend", "nextjs")
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "../out" in r.stdout


def test_frontend_dist_invente_echoue(tmp_path):
    p = write_conf(
        tmp_path,
        {
            "beforeDevCommand": "npm run dev",
            "beforeBuildCommand": "npm run build",
            "devUrl": "http://localhost:5173",
            "frontendDist": "../src",
        },
    )
    r = run(p, "--frontend", "vite")
    assert r.returncode != 0
    assert "frontenddist" in (r.stdout + r.stderr).lower()


def test_devurl_ssr_invente_echoue(tmp_path):
    p = write_conf(
        tmp_path,
        {
            "beforeDevCommand": "npm run dev",
            "beforeBuildCommand": "npm run build",
            "devUrl": "http://localhost:3000",
            "frontendDist": "../dist",
        },
    )
    r = run(p, "--frontend", "vite")
    assert r.returncode != 0
    assert "devurl" in (r.stdout + r.stderr).lower()


def test_nuxt_exige_generate(tmp_path):
    p = write_conf(
        tmp_path,
        {
            "beforeDevCommand": "npm run dev",
            "beforeBuildCommand": "npm run build",
            "devUrl": "http://localhost:3000",
            "frontendDist": "../dist",
        },
    )
    r = run(p, "--frontend", "nuxt")
    assert r.returncode != 0
    assert "generate" in (r.stdout + r.stderr).lower()


def test_leptos_exige_withglobaltauri(tmp_path):
    p = write_conf(
        tmp_path,
        {
            "beforeDevCommand": "trunk serve",
            "beforeBuildCommand": "trunk build",
            "devUrl": "http://localhost:1420",
            "frontendDist": "../dist",
        },
        app={},
    )
    r = run(p, "--frontend", "leptos")
    assert r.returncode != 0
    assert "withglobaltauri" in (r.stdout + r.stderr).lower()


def test_structure_projet_requise(tmp_path):
    root = tmp_path / "proj"
    (root / "src-tauri").mkdir(parents=True)
    conf_src = EXAMPLES / "tauri.conf.vite.json"
    assert conf_src.exists()
    (root / "src-tauri" / "tauri.conf.json").write_text(
        conf_src.read_text(encoding="utf-8"), encoding="utf-8"
    )
    r = run(root / "src-tauri" / "tauri.conf.json", "--project-root", str(root))
    assert r.returncode != 0
    assert "cargotoml" in (r.stdout + r.stderr).lower().replace(".", "").replace(
        " ", ""
    ) or "cargo" in (r.stdout + r.stderr).lower()
