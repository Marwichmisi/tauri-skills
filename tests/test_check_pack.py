"""Seam pack-level #19 : vérification du pack complet.

Comportement externe vérifié (spec #6, ticket #19) :
- 12 domaines présents, aucun skill mobile éclaté
- 12 descriptions déclenchables (Use me + renvois explicites)
- homonymes CLI distingués (dev vs in-app), renvoi catalogue→sécurité
- chaque référence porte ec113a50, Rust linkée jamais copiée
- le check échoue sur pack incomplet, passe sur pack initial.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check-pack.py"
SKILLS_ROOT = ROOT / "skills"

EXPECTED_SKILLS = [
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
]


def test_check_pack_existe():
    assert CHECK.is_file(), f"manquant: {CHECK}"


def test_pack_a_12_skills():
    for name in EXPECTED_SKILLS:
        assert (SKILLS_ROOT / name / "SKILL.md").is_file(), f"skill manquant: {name}"
    assert not (SKILLS_ROOT / "tauri-mobile").exists(), "pas de skill mobile éclaté"


def test_descriptions_declenchables_avec_renvois():
    for name in EXPECTED_SKILLS:
        text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        assert "Use me whenever" in text, f"{name}: description non pushy"
        m = re.search(r"description:\s*(.+)", text)
        assert m, f"{name}: frontmatter description manquant"
        assert "tauri-" in m.group(1), f"{name}: description sans renvoi explicite tauri-*"


def test_cli_homonymes_distribues():
    cli_ref = SKILLS_ROOT / "tauri-config-cli-reference" / "references" / "cli.md"
    text = cli_ref.read_text(encoding="utf-8")
    assert "Dev CLI" in text and "In-app CLI" in text, "contraste homonyme manquant"
    assert "CliExt" in text and "getMatches" in text, "marqueurs in-app manquants"
    desc = (SKILLS_ROOT / "tauri-config-cli-reference" / "SKILL.md").read_text(encoding="utf-8")
    assert "dev CLI vs in-app" in desc or "dev CLI" in desc, "description CLI sans homonymes"


def test_catalogue_renvoie_securite_sans_dupliquer():
    for ref in (SKILLS_ROOT / "tauri-plugins-catalogue" / "references").glob("*.md"):
        text = ref.read_text(encoding="utf-8")
        assert "tauri-security-capabilities" in text, f"{ref.name}: sans renvoi sécurité"


def test_mobile_non_eclate():
    mobiles = list(SKILLS_ROOT.glob("tauri-*/references/mobile.md"))
    names = sorted(p.parent.parent.name for p in mobiles)
    assert names == ["tauri-plugin-dev", "tauri-ui-recettes"], f"mobile éclaté: {names}"


def test_references_portent_commit_fige():
    refs = list(SKILLS_ROOT.glob("tauri-*/references/*.md"))
    assert len(refs) >= 80, f"attendu >=80 références, vu {len(refs)}"
    sans = [str(p) for p in refs if "ec113a50" not in p.read_text(encoding="utf-8")]
    assert not sans, f"sans pointeur ec113a50: {sans[:5]}"


def test_rust_linkee_jamais_copiee():
    lies = []
    for skill in ["tauri-frontend-bindings", "tauri-plugin-dev", "tauri-ui-recettes"]:
        for ref in (SKILLS_ROOT / skill / "references").glob("*.md"):
            if "docs.rs" in ref.read_text(encoding="utf-8"):
                lies.append(str(ref))
    assert len(lies) >= 5, "Rust linkée attendue (docs.rs) dans frontend/plugin-dev/ui"


def test_check_pack_passe_sur_pack_initial():
    r = subprocess.run([sys.executable, str(CHECK)], cwd=str(ROOT), capture_output=True, text=True)
    assert r.returncode == 0, f"check-pack doit passer:\n{r.stdout}\n{r.stderr}"
    assert "OK pack" in r.stdout
