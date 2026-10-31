# Transcript — WebDriver Tauri v2 (baseline, sans skill)

- Contexte : aucune input file, réponse rédigée de mémoire (connaissance générale Tauri v2 + WebdriverIO).
- Config embarquée : service WDIO `tauri` avec `application`/`appBinaryPath` vers
  `src-tauri/target/release/my-tauri-app`, capability `browserName: 'wry'` +
  `tauri:options.application`, sans hostname/port (driver géré par le service).
- Config manuelle : pas de service, `hostname 127.0.0.1` + `port 4444`,
  même capability `tauri:options`, `spawn('tauri-driver --port 4444')` dans
  `onBeforeSession`, kill dans `onAfterSession`/`onComplete`, compatible
  Windows (`shell: true`, `.exe`) et Linux.
- CI : workflow matrix Ubuntu/Windows, `cargo install tauri-driver`,
  `webkit2gtk-driver` + `xvfb` (+ `xvfb-run`) sur Linux,
  `msedgedriver-tool` sur Windows, `npx tauri build` puis `wdio run`.
- Aucune doc externe consultée, aucun test exécuté (pas de binaire ni de
  navigateur dans cet environnement) ; fichiers écrits tels quels dans `outputs/`.
