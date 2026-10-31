---
name: tauri-dev-quality
description: Debug and test a Tauri v2 app reproducibly (IDE debug, Linux graphics, CrabNebula DevTools, frontend mocking, WebDriver E2E + CI). Use me whenever the agent debugs the Core process, sets up launch/tasks/dap configs, works around WebKitGTK/NVIDIA, mocks Tauri APIs, or wires WebdriverIO/Selenium/tauri-driver/CI — I own the dev-quality doctrine, no invented tooling. Config schema lives in tauri-config-cli-reference, IPC code in tauri-ipc-bridge.
---

# Tauri Dev Quality

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (debug core vs IDE vs linux vs devtools vs mock vs webdriver/CI).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-dev-quality.py` avec le mode du tableau pour valider tout artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Débugger (dev-only `cfg(dev)`, consoles Rust/WebView, `open_devtools`, `build --debug`, feature `devtools`) | `references/debugging.md` | — (snippets doc, `RUST_BACKTRACE=1`) | — (renvoi doc) |
| Débugger dans VS Code / RustRover / Neovim (lldb, Cargo attach, dap, overseer) | `references/ide-debug.md` | `examples/launch.json`, `examples/tasks.json`, `examples/nvim-dap.lua` | `scripts/check-dev-quality.py --vscode` |
| Contourner un rendu Linux (blanc/flicker/crash, DMABUF, `Error 71`, WebGL silencieux) | `references/linux-graphics.md` | `examples/linux-workaround.rs` | `scripts/check-dev-quality.py --linux` |
| Instrumenter avec CrabNebula DevTools (logs, spans, commands, events) | `references/devtools.md` | `examples/crabnebula-devtools.rs` | — (renvoi doc, `cargo add tauri-plugin-devtools@2.0.0`) |
| Mocker Tauri en tests frontend (`mockIPC`, `mockWindows`, `clearMocks`, events partiels) | `references/mocking.md` | `examples/mock-ipc.js` | `scripts/check-dev-quality.py --mock` |
| Tester E2E WebDriver (service embarqué vs `tauri-driver` manuel, Selenium/WDIO, CI) | `references/webdriver.md` | `examples/wdio-service.conf.js`, `examples/wdio-manual.conf.js`, `examples/selenium-test.js`, `examples/webdriver.yml` | `scripts/check-dev-quality.py --wdio` + `--ci` |
| Doute inter-skill (schéma config complet, scope/capability, code IPC, fiche plugin) | voir Frontières | — | — |

## Frontières

- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet et CLI (`tauri dev/build/icon`, env-vars). Ici on ne montre que `beforeDevCommand` cité par les Run configs et `cargo test` avant e2e.
- `tauri-security-capabilities` : capabilities/permissions/scopes et durcissement. Ici aucune permission inventée, la doctrine vit là-bas.
- `tauri-ipc-bridge` : implémentation commands/events/state/resources/sidecar. Ici côté test (`mockIPC` fake `invoke` sans webview réelle, `browser.tauri.mock()` en E2E) ; le code d'appel part là-bas.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-plugin-dev`, `tauri-distribution`, `tauri-ui-recettes`, `tauri-plugins-catalogue`, `tauri-frontend-bindings` : hors périmètre debug/test ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun outillage inventé. Valeurs documentées seules : `lldb`/`cppvsdbg`, `--manifest-path=./src-tauri/Cargo.toml`, `--no-default-features` (dev), `mockIPC`/`mockWindows`/`clearMocks`, `driverProvider embedded/external/crabnebula`, `tauri:options` + `application`, `WEBKIT_DISABLE_DMABUF_RENDERER` / `WEBKIT_DISABLE_COMPOSITING_MODE` / `__NV_DISABLE_EXPLICIT_SYNC`, `tauri-plugin-devtools@2.0.0`.
- Route manuelle = Windows/Linux seuls (pas de driver desktop macOS, service embarqué requis) ; `WEBKIT_*` sous `#[cfg(target_os = "linux")]` ; `clearMocks` après chaque run ; `emitTo`/`emit_filter` non supportés.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Debug VS Code : `examples/launch.json` + `examples/tasks.json` (tirés de `develop/Debug/vscode.mdx`).
Valider avec `python3 scripts/check-dev-quality.py --vscode examples/launch.json`.
Mock : `examples/mock-ipc.js` (tiré de `develop/Tests/mocking.mdx`).
Valider avec `python3 scripts/check-dev-quality.py --mock examples/mock-ipc.js`.
WebDriver : `examples/wdio-service.conf.js` (service, `develop/Tests/WebDriver/index.mdx`) ou `examples/wdio-manual.conf.js` (manuel, `.../Example/webdriverio.mdx`) + `examples/webdriver.yml` (`.../ci.md`).
Valider avec `python3 scripts/check-dev-quality.py --wdio <conf> --ci examples/webdriver.yml` (deux appels).
