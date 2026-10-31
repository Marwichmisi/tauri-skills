# WebDriver — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/index.mdx` (titre `WebDriver`)
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/manual-setup.mdx` (titre `Manual setup`)
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/ci.md` (titre `Continuous Integration`)
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/Example/webdriverio.mdx` (titre `WebdriverIO`)
- `tauri-docs/src/content/docs/develop/Tests/WebDriver/Example/selenium.mdx` (titre `Selenium`)

## Route recommandée : service (index.mdx)

> The recommended way to use it with Tauri is [WebdriverIO] and the [`@wdio/tauri-service`], which works on **Windows, Linux, and macOS**.

Service = serveur WebDriver **embarqué** dans l'app (défaut, macOS OK, aucun driver externe), ou `external`/`crabnebula` (clé API payante, fork cross-platform). Détecte le binaire, sync Edge Driver sur Windows. Accès backend `browser.tauri.execute()`, mock IPC, capture logs, multiremote.

Scaffold : `npm create wdio@latest ./` → **Desktop Testing** → **Tauri**. Config minimale (même fichier), voir `examples/wdio-service.conf.js` :

```typescript
export const config: WebdriverIO.Config = {
  services: [['tauri', { appBinaryPath: './src-tauri/target/release/my-tauri-app', driverProvider: 'embedded' }]],
};
```

Plugins : `tauri-plugin-wdio-webdriver` (serveur embarqué, requis provider `embedded`) + `tauri-plugin-wdio` (backend `execute()`, mock, logs), optionnels selon besoins. Mode browser (renderer seul, Chrome + Vite dev-server, sans binaire/driver/plugin, `invoke()` intercepté) : voir browser-mode guide (lien doc uniquement). Exemples complets : fixtures `webdriverio/desktop-mobile`.

Check : `python3 scripts/check-dev-quality.py --wdio examples/wdio-service.conf.js`.

## Route manuelle : tauri-driver direct (manual-setup.mdx)

> Reach for it if you are not using Node.js, prefer [Selenium], or are integrating WebDriver into a custom test harness.

Desktop **Windows + Linux seuls** (macOS sans driver WKWebView ; iOS/Android via Appium 2 non streamlined). Pour la plupart : préférer le service (automatise tout + macOS).

- `cargo install tauri-driver --locked`.
- Linux : `WebKitWebDriver` (`which`, sinon `webkit2gtk-driver` Debian).
- Windows : Edge Driver matchant la version Edge (`msedgedriver-tool` : `cargo install --git https://github.com/chippers/msedgedriver-tool`, binaire `msedgedriver.exe` dans `$PATH` ou `--native-driver`).
- Selenium : `Builder().withCapabilities(tauri:options {application}).usingServer('http://127.0.0.1:4444/').build()`, `browserName wry` (voir selenium.mdx `test/test.js`).
- WebdriverIO manuel : `host 127.0.0.1`, `port 4444`, `specs ./test/specs/**/*.js`, `capabilities tauri:options {application: ../src-tauri/target/debug/tauri-app}`, `onPrepare` build `--debug --no-bundle`, `beforeSession` spawn `~/.cargo/bin/tauri-driver`, `afterSession`/shutdown cleanup (voir `examples/wdio-manual.conf.js`, copie fidèle).

Check : `python3 scripts/check-dev-quality.py --wdio examples/wdio-manual.conf.js`.

## Exemples Selenium / WebdriverIO (selenium.mdx, webdriverio.mdx)

- `e2e-tests/` dédié (`mkdir e2e-tests`). Deps selenium : `mocha chai selenium-webdriver`, script `test: mocha`, fichier `test/test.js` (build app `yarn tauri build --debug --no-bundle` timeout 120s, spawn tauri-driver, `findElement(By.css('body > h1'))`, luma `< 100`). Deps wdio : `@wdio/cli ^9.19.0` + local-runner/mocha-framework/spec-reporter, script `test: wdio run wdio.conf.js`, spec `test/specs/example.e2e.js` (`$`, `describe/it/expect`, luma helper).
- Tip doc wdio : le guide manuel montre les pièces ; la plupart doivent utiliser `@wdio/tauri-service` (automatise + macOS).

## CI (ci.md)

Hypothèses : app `src-tauri/`, runner WebdriverIO `e2e-tests/` (`yarn test`). Linux via faux display, Windows direct. Voir `examples/webdriver.yml` (copie exacte) : matrix `[ubuntu-latest, windows-latest]`, `webkit2gtk-driver + xvfb` (Linux), `msedgedriver-tool` (Windows), `dtolnay/rust-toolchain@stable` + `Swatinem/rust-cache@v2` (`src-tauri`), `cargo test` avant e2e, Node 24 + `yarn install --frozen-lockfile` (racine + `e2e-tests`), `cargo install tauri-driver --locked`, `xvfb-run yarn test` (Linux) / `yarn test` (Windows).

Check : `python3 scripts/check-dev-quality.py --ci examples/webdriver.yml`.
