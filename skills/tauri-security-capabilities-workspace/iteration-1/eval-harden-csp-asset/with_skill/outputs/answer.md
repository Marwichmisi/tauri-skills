# Durcissement : CSP minimale + assetProtocol $APPCACHE sauf secrets

Config minimale livrée dans `tauri.conf.json` (ce dossier) : snippet `app.security.csp` + `app.security.assetProtocol` uniquement.

## Ce qui est appliqué

**CSP** — `app.security.csp` :
- `default-src: 'self' customprotocol: asset:`
- `connect-src: ipc: http://ipc.localhost`
- `img-src: 'self' asset: http://asset.localhost blob: data:`
- `style-src: 'unsafe-inline' 'self'`
- Version volontairement minimale : pas de `font-src` / `https://fonts.googleapis.com` (présents dans l'exemple `api` complet). N'ajouter du distant que si nécessaire.
- Rappel doc : la protection CSP n'est active que si elle est définie dans le fichier de config ; Tauri ajoute automatiquement nonces/hashes au build. Éviter les scripts distants type CDN. Si WebAssembly, ajouter `'wasm-unsafe-eval'` en `script-src`.

**assetProtocol** — `app.security.assetProtocol` (forme objet, seule forme permettant `deny`) :
- `enable: true`
- `scope.allow: ["$APPCACHE/**/*"]`
- `scope.deny: ["$APPCACHE/**/secrets/**"]`
- `deny` gagne sur `allow` en cas de chevauchement.
- Sur Unix, `requireLiteralLeadingDot` vaut `true` par défaut : `*`/`**` ne matchent pas les segments à `.` (ex `.cache`). Non modifié ici (exposition minimale) ; ne passer à `false` qu'après revue car cela élargit l'exposition.

## Sources (commit ec113a50, EN canonique seule)

- `tauri-docs/src/content/docs/security/csp.mdx` (titre `Content Security Policy (CSP)`) — extraits : « The CSP protection is only enabled if set on the Tauri configuration file. At compile time, Tauri appends its nonces and hashes… », « Avoid loading remote content such as scripts served over a CDN… include `'wasm-unsafe-eval'` as `script-src` », + exemple `tauri/examples/api/src-tauri/tauri.conf.json` (`default-src`, `connect-src`, `img-src`, `style-src`).
- `tauri-docs/src/content/docs/security/asset-protocol.mdx` (titre `Asset protocol scope`) — extraits : « Whether a path is allowed is controlled by **`app.security.assetProtocol`**… You must set **`enable`** to `true` and define a **`scope`**. », forme objet `allow: ["$APPCACHE/**/*"]` / `deny: ["$APPCACHE/**/secrets/**"]`, « `deny` takes precedence over `allow` », `requireLiteralLeadingDot` défaut `true` sur Unix.
- Routage skill : `skills/tauri-security-capabilities/references/hardening.md` (agrège csp / asset-protocol / http-headers / lifecycle / index).

## Frontière — renvoi tauri-config-cli-reference

- Le schéma **complet** de `tauri.conf.json` / `gen/schemas` (tous les champs, types Rust `AssetProtocolConfig`/`FsScope`, rendu `reference/config/`) est du ressort de **`tauri-config-cli-reference`**. Ici seul le snippet `security.csp` / `security.assetProtocol` est montré, sans dupliquer le schéma.
- `capabilities` non couvertes ici (voir `references/capabilities.md` + `examples/default-capability.json`, validation `scripts/check-capabilities.py`). Headers (`http-headers.mdx`, depuis 2.1.0) et lifecycle hors scope de cette demande.
- API Rust linkée, jamais copiée ; traductions ignorées.
