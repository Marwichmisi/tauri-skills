# Transcript

1. Lu `skills/tauri-dev-quality/SKILL.md` → routage WebDriver : lire `references/webdriver.md`, exemples `wdio-service.conf.js` / `wdio-manual.conf.js` / `webdriver.yml`, script `scripts/check-dev-quality.py --wdio` + `--ci`.
2. Lu `references/webdriver.md` (sources commit ec113a50 : `develop/Tests/WebDriver/index.mdx`, `manual-setup.mdx`, `ci.md`, `Example/webdriverio.mdx`, `Example/selenium.mdx`).
3. Lu les 3 exemples + le script de check (règles wdio : service `tauri` + `appBinaryPath` + `embedded/external/crabnebula` OU manuelle `tauri-driver` spawn + `tauri:options` + `application` ; ci : `tauri-driver` + `webkit2gtk-driver/xvfb` ou `msedgedriver-tool` + `xvfb-run yarn test`).
4. Écrit `outputs/wdio-service.conf.js` (service `tauri`, `appBinaryPath: ./src-tauri/target/release/my-tauri-app`, `driverProvider: embedded`).
5. Écrit `outputs/wdio-manual.conf.js` (copie fidèle : `127.0.0.1:4444`, `tauri:options.application`, spawn `~/.cargo/bin/tauri-driver`, `onPrepare build --debug --no-bundle`).
6. Écrit `outputs/webdriver.yml` (copie exacte : matrix ubuntu/windows, `webkit2gtk-driver+xvfb`, `msedgedriver-tool`, `xvfb-run yarn test`).
7. Exécuté :
   - `python3 scripts/check-dev-quality.py --wdio outputs/wdio-service.conf.js` → `OK ... wdio route service fidèle` (exit 0)
   - `python3 scripts/check-dev-quality.py --wdio outputs/wdio-manual.conf.js` → `OK ... wdio route manuelle fidèle` (exit 0)
   - `python3 scripts/check-dev-quality.py --ci outputs/webdriver.yml` → `OK ... CI webdriver fidèle` (exit 0)
8. Écrit `outputs/answer.md` (explication + sources commit ec113a50, mention manuel hors macOS) et le présent `transcript.md`.
