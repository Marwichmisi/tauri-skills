# Test frontend Vitest — Mock `add` + fenêtres (baseline sans skill)

## Réponse

Le fichier `mock-test.js` fournit un test Vitest complet qui :

1. **Shim WebCrypto jsdom inclus** : importe `webcrypto` depuis `node:crypto` et l'assigne à `globalThis.crypto` si absent. Nécessaire car `jsdom` n'expose pas `crypto.subtle`, ce qui fait échouer `@tauri-apps/api` qui vérifie la disponibilité crypto au chargement.

2. **Espion `invoke` mockant la commande `add`** :
   - `vi.mock('@tauri-apps/api/core', () => ({ invoke: vi.fn() }))`
   - `invoke.mockImplementation((cmd, args) => ...)` retourne `27` pour `('add', {a:12, b:15})`, sinon `a+b`.
   - Assertions : `expect(result).toBe(27)`, `toHaveBeenCalledTimes(1)`, `toHaveBeenCalledWith('add', {a:12,b:15})`.

3. **Mock des fenêtres `main` / `second` / `third`** :
   - `vi.mock('@tauri-apps/api/webviewWindow', ...)` avec `getAllWebviewWindows` résolvant 3 fenêtres mockées (`label` + `close/show/hide` en `vi.fn()`), `getCurrentWebviewWindow` retournant `main`, et `WebviewWindow` mocké.
   - Test : `listWindowLabels()` retourne `['main','second','third']`.

4. **Clear les mocks après chaque run** :
   - `beforeEach(() => vi.clearAllMocks())` + `afterEach(() => vi.clearAllMocks())` pour garantir l'isolation entre tests.
   - 3e test vérifie que `invoke` repart à zéro (`not.toHaveBeenCalled()` en début de test).

## Exécution

```bash
npm i -D vitest jsdom
npx vitest run mock-test.js --environment jsdom
```

Fichier : `mock-test.js` (même dossier).
