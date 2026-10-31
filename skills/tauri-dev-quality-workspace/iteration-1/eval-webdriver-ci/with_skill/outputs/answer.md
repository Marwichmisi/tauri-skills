# Tests E2E WebDriver — app Tauri v2 (`src-tauri/target/release/my-tauri-app`)

## 1. Route recommandée : service embarqué (`wdio-service.conf.js`)

Copie fidèle de `examples/wdio-service.conf.js` (skill `tauri-dev-quality`) :

```js
export const config = {
  services: [
    ["tauri", {
      appBinaryPath: "./src-tauri/target/release/my-tauri-app",
      driverProvider: "embedded",
    }],
  ],
};
```

- `services: [['tauri', ...]]` + `appBinaryPath` + `driverProvider: 'embedded'` : combinaison exigée par le check `--wdio`.
- `embedded` = serveur WebDriver embarqué dans l'app (défaut doc). Variantes documentées seules : `external` / `crabnebula` (clé API payante). Aucune autre valeur.
- Plugins optionnels selon besoins : `tauri-plugin-wdio-webdriver` (requis pour `embedded`) + `tauri-plugin-wdio` (backend `execute()`, mock, logs).
- Scaffold doc : `npm create wdio@latest ./` → **Desktop Testing** → **Tauri**.
- Fonctionne sur **Windows, Linux et macOS**.

## 2. Variante manuelle Windows/Linux (`wdio-manual.conf.js`)

Copie fidèle de `examples/wdio-manual.conf.js`. Points clés :

- `host: "127.0.0.1"`, `port: 4444`, `specs: ["./test/specs/**/*.js"]`.
- `capabilities` avec `tauri:options` + `application` (binaire debug buildé par `onPrepare` : `build --debug --no-bundle`).
- `beforeSession` : `spawn(~/.cargo/bin/tauri-driver)` ; `afterSession` : cleanup (`kill()`).
- Prérequis doc :
  - `cargo install tauri-driver --locked`.
  - Linux : `WebKitWebDriver` (`webkit2gtk-driver` sur Debian).
  - Windows : Edge Driver versionné (`cargo install --git https://github.com/chippers/msedgedriver-tool`, binaire dans `$PATH` ou `--native-driver`).
- Variante Selenium (même doctrine) : `Builder().withCapabilities(tauri:options {application}).usingServer('http://127.0.0.1:4444/')`, `browserName wry`.

> **Le manuel ne couvre pas macOS.** Pas de driver desktop macOS (WKWebView) ; iOS/Android via Appium 2 non streamlined. Pour macOS, utiliser obligatoirement la route service embarquée ci-dessus.

## 3. CI (`webdriver.yml`)

Copie exacte de `examples/webdriver.yml`. Hypothèses doc : app en `src-tauri/`, runner WebdriverIO en `e2e-tests/` lancé par `yarn test` :

- Matrix `[ubuntu-latest, windows-latest]`, `on: [push]`.
- Linux : `webkit2gtk-driver + xvfb` (`libwebkit2gtk-4.1-dev`, `libayatana-appindicator3-dev`), run `xvfb-run yarn test`.
- Windows : `msedgedriver-tool` (`cargo install --git ...`), run `yarn test` direct.
- Commun : `dtolnay/rust-toolchain@stable` + `Swatinem/rust-cache@v2` (`src-tauri`), `cargo test` avant e2e, Node 24 + `yarn install --frozen-lockfile` (racine + `e2e-tests`), `cargo install tauri-driver --locked`.

## 4. Validation `check-dev-quality.py`

```
OK .../outputs/wdio-service.conf.js: wdio route service fidèle
---SERVICE_EXIT:0
OK .../outputs/wdio-manual.conf.js: wdio route manuelle fidèle
---MANUAL_EXIT:0
OK .../outputs/webdriver.yml: CI webdriver fidèle
---CI_EXIT:0
```

Commandes :
```
python3 scripts/check-dev-quality.py --wdio outputs/wdio-service.conf.js
python3 scripts/check-dev-quality.py --wdio outputs/wdio-manual.conf.js
python3 scripts/check-dev-quality.py --ci outputs/webdriver.yml
```

## Sources (commit `ec113a50`, EN canonique seule)

- `tauri-docs/src/content/docs/develop/Tests/WebDriver/index.mdx` (titre `WebDriver`) — route service, `appBinaryPath` + `driverProvider embedded/external/crabnebula`, Windows/Linux/macOS.
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/manual-setup.mdx` (titre `Manual setup`) — `tauri-driver`, `webkit2gtk-driver`, `msedgedriver-tool`, Windows/Linux seuls.
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/ci.md` (titre `Continuous Integration`) — matrix, `webkit2gtk-driver`/`xvfb`, `msedgedriver-tool`, `xvfb-run yarn test`.
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/Example/webdriverio.mdx` (titre `WebdriverIO`) — config manuelle `127.0.0.1:4444`, `tauri:options` + `application`, spawn `tauri-driver`.
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/Example/selenium.mdx` (titre `Selenium`) — `tauri:options`, `usingServer 127.0.0.1:4444`, `browserName wry`.
- Skill : `skills/tauri-dev-quality/references/webdriver.md`, exemples `examples/wdio-service.conf.js`, `examples/wdio-manual.conf.js`, `examples/webdriver.yml`.

Aucun outillage inventé. Valeurs hors doc ignorées.
