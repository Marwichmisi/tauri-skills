# Test frontend Vitest — mock `add` (12+15=27)

## Explication

Test Vitest utilisant le mock runtime frontend (`@tauri-apps/api/mocks`), sans
webview native réelle :

1. **Shim WebCrypto jsdom** (`beforeAll`) : jsdom ne fournit pas WebCrypto, on
   branche `window.crypto.getRandomValues` sur `randomFillSync` de `node:crypto`.
2. **`mockIPC((cmd, args) => ...)`** : intercepte `invoke`. La commande simulée
   `add` retourne `args.a + args.b`, donc `invoke("add", { a: 12, b: 15 })`
   résout `27`.
3. **Espion `invoke`** : `vi.spyOn(window.__TAURI_INTERNALS__, "invoke")` puis
   `expect(spy).toHaveBeenCalled()` — outillage d'espionnage Vitest documenté.
4. **`mockWindows('main', 'second', 'third')`** : le 1er label (`main`) est la
   fenêtre courante ; les autres sont additionnelles. Ne fake que l'existence
   des fenêtres, pas leurs propriétés (celles-ci passent par `mockIPC`).
   Vérifié via `getCurrent()` / `getAll()` de `@tauri-apps/api/webviewWindow`.
5. **`clearMocks()` dans `afterEach`** : exigé par la doc pour annuler les
   changements d'état mock entre runs.

Fichier : `mock-test.js` (assemblage fidèle des snippets, imports exacts).

## Validation script

```
$ python3 skills/tauri-dev-quality/scripts/check-dev-quality.py --mock mock-test.js
OK mock-test.js: mock fidèle (mocking.mdx)
```

## Sources (commit `ec113a50`, EN canonique seule)

- `tauri-docs/src/content/docs/develop/Tests/mocking.mdx` (titre `Mock Tauri APIs`)
  — `mockIPC`, `mockWindows`, `clearMocks`, module `@tauri-apps/api/mocks` ;
  exemples Vitest transposables à jest ; `clearMocks()` après chaque run ;
  `mockWindows('main', 'second', 'third')` ; shim WebCrypto jsdom
  (`randomFillSync`, `getRandomValues`).
- `tauri-docs/src/content/docs/develop/Tests/index.mdx` (titre `Tests`) —
  panorama : mock runtime (pas de webview native) vs E2E WebDriver.
- Skill : `skills/tauri-dev-quality/references/mocking.md`,
  exemple `skills/tauri-dev-quality/examples/mock-ipc.js`.

## Frontière E2E (app réelle)

En E2E (app réelle ou frontend navigateur), le mock équivalent n'est **pas**
`mockIPC` mais **`browser.tauri.mock()`** de `@wdio/tauri-service`
(voir `references/webdriver.md`, skill frère `tauri-ipc-bridge` pour le code
d'appel). Aucune API mock inventée : seules `mockIPC` / `mockWindows` /
`clearMocks` sont utilisées.
