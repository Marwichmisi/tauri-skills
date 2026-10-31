# IPC Pattern : Brownfield vs Isolation — Recommandation

## Verdict : Passer en Isolation

Frontend avec **centaines de dépendances imbriquées** + appels API Tauri sensibles (lecture fichier, fetch HTTP) = frontend **non fiable**.

Rester en **brownfield** = le frontend a accès direct à `window.__TAURI__` / `invoke()`. Une seule dépendance compromise (XSS, supply-chain, prototype-pollution) peut appeler `read_file`, exfiltrer via `fetch`, et élever les privilèges. Brownfield ne convient que si le frontend est petit, audité, sans dépendances tierces risquées.

**Isolation** : le frontend tourne dans une `<iframe>` sandboxée sans accès direct à l'API Tauri. Tout IPC passe par un hook isolé, petit et auditable, qui whitelist les commandes.

## Config `tauri.conf.json` (pattern choisi : isolation)

Voir fichier `tauri.conf.json` joint. Points clés :

```json
"pattern": {
  "use": "isolation",
  "options": { "dir": "../dist-isolation" }
}
```

+ `capabilities` / `allowlist` resserrées au strict minimum (pas de `all: true`, pas de `shell.open` générique, pas de `fs.readFile` sans scope).

## Hook minimal

Voir `hook.js`. Principe : `window.__TAURI_ISOLATION_HOOK__` intercepte chaque message, vérifie `cmd` contre une allowlist, valide/sanitize les args (chemins, URLs), puis laisse passer ou rejette.

## Limites de l'Isolation

1. **Pas de sécurité magique** : si le hook autorise `read_file:*` ou `http:*`, l'isolation ne sert à rien. La sécurité repose sur la whitelist + validation des args dans le hook.
2. **Pas d'accès direct** : le frontend isolé ne peut plus appeler `invoke()` directement. Tout passe en `postMessage` asynchrone via le hook. Code frontend à adapter.
3. **Double build** : il faut builder `dist/` (app) + `dist-isolation/` (index.html + hook.js). `dir` doit exister au build sinon erreur.
4. **Debug plus dur** : DevTools, stacktraces et erreurs IPC sont cloisonnés entre iframe et hook. Prévoir logs explicites dans le hook.
5. **Perf / overhead** : sérialisation + chiffrement AES-GCM du pont isolé sur chaque appel. Ne pas y faire transiter de gros binaires à haute fréquence ; préférer streaming/chunk + limites de taille.
6. **Hook = TCB** : le hook doit rester minimal (<100 lignes), sans dépendances npm, audité. Toute lib ajoutée dans `dist-isolation` annule le bénéfice.
7. **Compléter par** : CSP stricte, `capabilities` par fenêtre, validation côté Rust (`#[tauri::command]` vérifie chemin/URL), pas de secrets dans le frontend.
