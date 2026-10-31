"""Seam basse tauri-dev-quality : check déterministe debug et tests.

Vérifie le comportement externe de l'agent avec le skill (setup fidèle
à la doc), jamais les détails internes du skill.

Référence : ticket #12, gabarit docs/gabarit-skill.md, étalon repris du
pilote skills/tauri-security-capabilities/scripts/check-capabilities.py.

Couvre (5 modes) :
- --mock fichier JS : mockIPC/mockWindows/clearMocks issus de
  @tauri-apps/api/mocks uniquement, clearMocks exigé, shouldMockEvents
  seulement avec mockIPC.
- --wdio conf JS : route service (@wdio/tauri-service, appBinaryPath +
  driverProvider embedded/external/crabnebula) OU route manuelle
  (tauri-driver + tauri:options + application), jamais d'outillage inventé.
- --vscode launch.json : type lldb/cppvsdbg, cargo manifest-path
  src-tauri/Cargo.toml, preLaunchTask, --no-default-features en dev.
- --ci workflow yml : tauri-driver + webkit2gtk-driver/xvfb (linux) ou
  msedgedriver-tool (windows), xvfb-run.
- --linux snippet rs : vars documentées seules, garde cfg linux exigée.
"""
import pathlib
import subprocess
import sys

SKILL = pathlib.Path(__file__).resolve().parents[1]
CHECK = SKILL / "scripts" / "check-dev-quality.py"
EXAMPLES = SKILL / "examples"


def run(*args):
    r = subprocess.run(
        [sys.executable, str(CHECK), *[str(a) for a in args]],
        capture_output=True,
        text=True,
    )
    return r


def test_exemple_mock_ok_passe():
    p = EXAMPLES / "mock-ipc.js"
    assert p.exists(), f"manquant: {p}"
    r = run("--mock", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_mock_sans_clearmocks_echoue(tmp_path):
    p = tmp_path / "bad.js"
    p.write_text(
        'import { mockIPC } from "@tauri-apps/api/mocks";\n'
        "mockIPC((cmd) => { if (cmd === 'add') return 1; });\n",
        encoding="utf-8",
    )
    r = run("--mock", p)
    assert r.returncode != 0
    assert "clearmocks" in (r.stdout + r.stderr).lower().replace(" ", "")


def test_mock_api_inventee_echoue(tmp_path):
    p = tmp_path / "bad.js"
    p.write_text(
        'import { mockFakeWindow } from "@tauri-apps/api/mocks";\n'
        "import { clearMocks } from '@tauri-apps/api/mocks';\n"
        "mockFakeWindow('main');\n",
        encoding="utf-8",
    )
    r = run("--mock", p)
    assert r.returncode != 0
    assert "mock" in (r.stdout + r.stderr).lower()


def test_exemple_wdio_service_ok_passe():
    p = EXAMPLES / "wdio-service.conf.js"
    assert p.exists(), f"manquant: {p}"
    r = run("--wdio", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_exemple_wdio_manual_ok_passe():
    p = EXAMPLES / "wdio-manual.conf.js"
    assert p.exists(), f"manquant: {p}"
    r = run("--wdio", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_wdio_sans_tauri_echoue(tmp_path):
    p = tmp_path / "bad.js"
    p.write_text(
        "export const config = { framework: 'mocha', specs: ['./test/*.js'] };\n",
        encoding="utf-8",
    )
    r = run("--wdio", p)
    assert r.returncode != 0
    assert "tauri" in (r.stdout + r.stderr).lower()


def test_exemple_vscode_ok_passe():
    p = EXAMPLES / "launch.json"
    assert p.exists(), f"manquant: {p}"
    r = run("--vscode", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_vscode_type_invente_echoue(tmp_path):
    import json

    p = tmp_path / "launch.json"
    p.write_text(
        json.dumps(
            {
                "version": "0.2.0",
                "configurations": [
                    {
                        "type": "node",
                        "request": "launch",
                        "name": "Bad",
                        "program": "app",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    r = run("--vscode", p)
    assert r.returncode != 0
    assert "type" in (r.stdout + r.stderr).lower()


def test_exemple_ci_ok_passe():
    p = EXAMPLES / "webdriver.yml"
    assert p.exists(), f"manquant: {p}"
    r = run("--ci", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_ci_sans_tauri_driver_echoue(tmp_path):
    p = tmp_path / "ci.yml"
    p.write_text("jobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: yarn test\n", encoding="utf-8")
    r = run("--ci", p)
    assert r.returncode != 0
    assert "tauri-driver" in (r.stdout + r.stderr).lower()


def test_exemple_linux_ok_passe():
    p = EXAMPLES / "linux-workaround.rs"
    assert p.exists(), f"manquant: {p}"
    r = run("--linux", p)
    assert r.returncode == 0, f"OK attendu:\n{r.stdout}\n{r.stderr}"
    assert "OK" in r.stdout


def test_linux_var_inventee_echoue(tmp_path):
    p = tmp_path / "bad.rs"
    p.write_text('std::env::set_var("WEBKIT_FAKE_RENDERER", "1");\n', encoding="utf-8")
    r = run("--linux", p)
    assert r.returncode != 0
    assert "webkit" in (r.stdout + r.stderr).lower() or "var" in (r.stdout + r.stderr).lower()
