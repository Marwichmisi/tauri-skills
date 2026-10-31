# Tests E2E WebDriver — Tauri v2 (`src-tauri/target/release/my-tauri-app`)

## 1. Prérequis

```bash
cargo install tauri-driver --locked
npm i -D @wdio/cli @wdio/local-runner @wdio/mocha-framework @wdio/spec-reporter wdio-tauri-service
npx tauri build   # produit src-tauri/target/release/my-tauri-app(.exe)
```

- Linux : `webkit2gtk-driver` + `xvfb` (`sudo apt install webkit2gtk-driver xvfb`).
- Windows : WebView2 (Edge) + `cargo install msedgedriver-tool --locked`.
- Le binaire doit exister avant les tests ; `appBinaryPath` / `tauri:options.application`
  pointent dessus en absolu.

## 2. Config service embarquée (`wdio-service.conf.js`)

```js
services: [['tauri', { application: appBinary }]]
capabilities: [{ browserName: 'wry', 'tauri:options': { application: appBinary } }]
```

WDIO démarre/arrête `tauri-driver` seul. Lancement :

```bash
npx wdio run wdio-service.conf.js
```

C'est la variante recommandée en local et en CI.

## 3. Variante manuelle Windows / Linux (`wdio-manual.conf.js`)

Pas de `services`. Connexion brute au driver :

```js
hostname: '127.0.0.1', port: 4444,
capabilities: [{ browserName: 'wry', 'tauri:options': { application: appBinary } }]
```

Le driver est spawné par `onBeforeSession` :

```js
spawn('tauri-driver', ['--port', '4444'])
```

ou à la main pour débugger :

```bash
tauri-driver --port 4444
npx wdio run wdio-manual.conf.js
```

Écoute sur `127.0.0.1:4444` (pas `localhost` : évite les résolutions IPv6).
`onAfterSession` / `onComplete` tuent le processus.

## 4. CI (`.github/workflows/webdriver.yml`)

- `cargo install tauri-driver --locked` sur tous les OS.
- Linux : `webkit2gtk-driver` + `xvfb`, tests sous `xvfb-run`.
- Windows : `cargo install msedgedriver-tool --locked`.
- `npx tauri build` puis `xvfb-run npx wdio run wdio-service.conf.js` (Linux)
  / `npx wdio run wdio-service.conf.js` (Windows).
- Variante manuelle : même job avec `wdio-manual.conf.js` (exemples commentés).

## 5. Fichiers fournis

- `wdio-service.conf.js` — service `tauri` + `appBinaryPath`/`application` + `embedded`.
- `wdio-manual.conf.js` — spawn `tauri-driver`, `tauri:options.application`, `127.0.0.1:4444`.
- `webdriver.yml` — job matrix Ubuntu/Windows avec tauri-driver, webkit2gtk-driver/xvfb,
  msedgedriver-tool, xvfb-run.
