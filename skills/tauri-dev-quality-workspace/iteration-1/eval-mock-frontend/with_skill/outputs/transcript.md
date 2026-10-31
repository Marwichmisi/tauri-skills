# Transcript

1. Lu `skills/tauri-dev-quality/SKILL.md` → intention « Mocker Tauri en tests
   frontend » → route `references/mocking.md`, exemple `examples/mock-ipc.js`,
   script `scripts/check-dev-quality.py --mock`.
2. Lu `references/mocking.md` (sources commit `ec113a50` :
   `develop/Tests/index.mdx` + `develop/Tests/mocking.mdx`) : `mockIPC` /
   `mockWindows` / `clearMocks`, espion `vi.spyOn(window.__TAURI_INTERNALS__,
   "invoke")`, `mockWindows('main', 'second', 'third')`, shim WebCrypto jsdom,
   `clearMocks` après chaque run, frontière `browser.tauri.mock()` en E2E.
3. Lu `examples/mock-ipc.js` (assemblage fidèle des snippets, imports exacts).
4. Écrit `mock-test.js` : mock `add` (12+15=27) avec espion invoke, mock
   fenêtres main/second/third, `clearMocks` en `afterEach`, shim WebCrypto
   jsdom inclus.
5. Exécuté `python3 scripts/check-dev-quality.py --mock mock-test.js` →
   `OK mock-test.js: mock fidèle (mocking.mdx)`.
6. Écrit `answer.md` (explication + sources + sortie check + frontière E2E) et
   le présent `transcript.md`.
