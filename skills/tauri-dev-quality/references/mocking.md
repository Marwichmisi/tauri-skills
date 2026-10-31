# Mocking — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Tests/index.mdx` (titre `Tests`)
- `tauri-docs/src/content/docs/develop/Tests/mocking.mdx` (titre `Mock Tauri APIs`)

## Panorama (index.mdx)

> Tauri offers support for both unit and integration testing utilizing a mock runtime. Under the mock runtime, native webview libraries are not executed.

> Tauri also provides support for end-to-end testing utilizing the WebDriver protocol.

`tauri-action` pour GitHub Actions, tout runner CI avec libs système Tauri accepté.

## Mock runtime (mocking.mdx)

> When writing your frontend tests, having a "fake" Tauri environment to simulate windows or intercept IPC calls is common, so-called _mocking_. The [`@tauri-apps/api/mocks`] module provides some helpful tools.

> Remember to clear mocks after each test run to undo mock state changes between runs! See [`clearMocks()`] docs for more info.

APIs documentées seules : `mockIPC`, `mockWindows`, `clearMocks` (module `@tauri-apps/api/mocks`). Exemples en Vitest, transposables à jest.

Voir `examples/mock-ipc.js` (assemblage fidèle des snippets, imports exacts) :

- `mockIPC` intercepte `invoke` (ex `add` → `a+b`), espionnable via `vi.spyOn(window.__TAURI_INTERNALS__, "invoke")`.
- Sidecar/shell : catcher `spawn()`/`execute()`, récupérer `_${args.message.onEventFn}`, émettre `Stdout` (répétable) puis `Terminated` (`{code: 0, signal: 'kill'}`) pour résoudre la promesse.
- `clearMocks()` après chaque run (`afterEach`).
- `mockWindows('main', 'second', 'third')` : 1er = fenêtre courante, autres = additionnelles. Ne fake que l'existence, pas les propriétés (passer par `mockIPC` pour elles).
- WebCrypto jsdom shim requis (`randomFillSync`, `getRandomValues`).
- Events (≥ 2.7.0, partiel) : `mockIPC(() => {}, { shouldMockEvents: true })` puis `listen`/`emit` ; `emitTo`/`emit_filter` **non supportés**.

Note doc : en E2E (app réelle ou frontend navigateur), le mock équivalent est `browser.tauri.mock()` de `@wdio/tauri-service`, pas `mockIPC` (voir `references/webdriver.md`).

Check : `python3 scripts/check-dev-quality.py --mock examples/mock-ipc.js`.
