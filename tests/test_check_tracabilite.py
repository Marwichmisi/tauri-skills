"""Seam haute pack-level : traçabilité 135 pages → domaines.

Comportement externe vérifié (spec #6, ticket #7) :
- chaque page EN canonique listée dans docs/tracabilite.json
- chaque entrée pointe vers un domaine connu (12 skills + hors-pack + généré)
- le check échoue sur page non couverte, passe sur mapping initial.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TRAC_FILE = ROOT / "docs" / "tracabilite.json"
CHECK = ROOT / "scripts" / "check-tracabilite.py"
DOCS_ROOT = ROOT / "tauri-docs" / "src" / "content" / "docs"

ALLOWED_SKILLS = {
    "tauri-start",
    "tauri-migrate",
    "tauri-core-concepts",
    "tauri-security-capabilities",
    "tauri-ipc-bridge",
    "tauri-dev-quality",
    "tauri-plugin-dev",
    "tauri-distribution",
    "tauri-ui-recettes",
    "tauri-plugins-catalogue",
    "tauri-config-cli-reference",
    "tauri-frontend-bindings",
    "hors-pack",
}


def load_mapping():
    assert TRAC_FILE.exists(), f"manquant: {TRAC_FILE}"
    data = json.loads(TRAC_FILE.read_text(encoding="utf-8"))
    assert "mapping" in data, "tracabilite.json doit contenir 'mapping'"
    return data


def test_mapping_couvre_135_pages():
    data = load_mapping()
    assert data["commit"] == "ec113a50", "commit figé attendu ec113a50"
    assert len(data["mapping"]) == 135, f"attendu 135 entrées, vu {len(data['mapping'])}"


def test_domaines_connus_uniquement():
    data = load_mapping()
    for path, skill in data["mapping"].items():
        assert skill in ALLOWED_SKILLS, f"{path} → domaine inconnu {skill!r}"


def test_check_passe_sur_mapping_initial():
    r = subprocess.run(
        [sys.executable, str(CHECK)], cwd=str(ROOT), capture_output=True, text=True
    )
    assert r.returncode == 0, f"check doit passer:\n{r.stdout}\n{r.stderr}"
    assert "135/135" in r.stdout or "135" in r.stdout


def test_check_echoue_sur_page_non_couverte(tmp_path, monkeypatch):
    # Simule une page orpheline : le check doit FAIL.
    import shutil

    fake_docs = tmp_path / "docs"
    shutil.copytree(str(DOCS_ROOT), str(fake_docs))
    # Ajoute une page non tracée
    (fake_docs / "security" / "page-fantome.mdx").write_text(
        "---\ntitle: Fantome\n---\n", encoding="utf-8"
    )
    r = subprocess.run(
        [sys.executable, str(CHECK), "--docs-root", str(fake_docs)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode != 0, "check doit échouer sur page non couverte"
    assert "page-fantome" in r.stdout + r.stderr
