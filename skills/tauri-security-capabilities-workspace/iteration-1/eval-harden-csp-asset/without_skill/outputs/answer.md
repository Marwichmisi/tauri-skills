# Durcissement : CSP minimale + assetProtocol ($APPCACHE sauf secrets)

## 1. Config appliquée (`tauri.conf.json`)

```json
"security": {
  "csp": "default-src 'self' customprotocol: asset: https://asset.localhost; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
  "freezePrototype": true,
  "dangerousDisableAssetCspModification": false,
  "assetProtocol": {
    "enable": true,
    "scope": {
      "allow": ["$APPCACHE/**"],
      "deny": ["$APPCACHE/**/secrets/**"]
    }
  }
}
```

## 2. Pourquoi cette CSP est minimale et dure

- `default-src 'self' customprotocol: asset: https://asset.localhost` : base fermée. `'self'` = HTML/JS du bundle, `asset:` + `https://asset.localhost` = obligatoire pour `convertFileSrc()` / `assetProtocol`, sinon images/fichiers locaux bloqués. `customprotocol:` = requis si protocole custom enregistré.
- `script-src 'self'` / `style-src 'self'` : pas de `unsafe-inline`, pas de `unsafe-eval`, pas de `http:`, pas de `*`, pas de CDN. Tout inline doit passer en fichier local ou nonce/hash (à ajouter si besoin framework).
- `object-src 'none'` : bloque `<object>/<embed>`, plugins.
- `base-uri 'none'` + `frame-ancestors 'none'` : anti base-hijack et anti clickjacking.
- `freezePrototype: true` : fige `Array/Object` contre prototype pollution.
- `dangerousDisableAssetCspModification: false` (défaut) : laisse Tauri injecter automatiquement `asset:` dans la CSP. Ne pas mettre à `true` sauf CSP 100% manuelle.

## 3. Pourquoi cet assetProtocol

- `enable: true` : active `asset://` / `https://asset.localhost`.
- `allow: ["$APPCACHE/**"]` : expose uniquement le dossier cache applicatif (`$APPCACHE`), pas `$APPDATA`, `$HOME`, `$RESOURCE`, etc.
- `deny: ["$APPCACHE/**/secrets/**"]` : prend le pas sur `allow`. Bloque tout sous-dossier `secrets/` à n'importe quelle profondeur. Ex : `$APPCACHE/user/secrets/token.json` => 403, même si `$APPCACHE/**` est autorisé.
- Frontend : toujours passer par `convertFileSrc(path)` de `@tauri-apps/api/core`, jamais de chemin absolu en dur.

## 4. Vérification

1. `npm run tauri dev` -> console WebView : aucune violation CSP sur page normale.
2. `fetch(convertFileSrc(APPCACHE + "/img.png"))` => 200.
3. `fetch(convertFileSrc(APPCACHE + "/secrets/key.json"))` ou `.../sub/secrets/x` => bloqué (asset scope deny).
4. Tester XSS inline `<script>alert(1)</script>` => bloqué par `script-src 'self'`.
5. `tauri build` sans warning `assetProtocol` / `csp`.

Ne pas stocker de vrais secrets en clair dans `$APPCACHE`, même avec `deny` : utiliser keychain / stronghold.
