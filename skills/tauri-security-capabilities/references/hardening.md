# Durcissement — CSP, asset-protocol, headers, lifecycle

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/security/csp.mdx` (titre `Content Security Policy (CSP)`)
- `tauri-docs/src/content/docs/security/asset-protocol.mdx` (titre `Asset protocol scope`)
- `tauri-docs/src/content/docs/security/http-headers.mdx` (titre `HTTP Headers`)
- `tauri-docs/src/content/docs/security/lifecycle.mdx` (titre `Application Lifecycle Threats`)
- `tauri-docs/src/content/docs/security/index.mdx` (titre `Security`, trust boundaries)

## CSP (csp.mdx)

> Tauri restricts the Content Security Policy of your HTML pages. Local scripts are hashed, styles and external scripts are referenced using a cryptographic nonce.
> The CSP protection is only enabled if set on the Tauri configuration file. At compile time, Tauri appends its nonces and hashes to the relevant CSP attributes automatically.

Exemple canonique (même fichier, `tauri/examples/api/src-tauri/tauri.conf.json`) :

```json
"csp": {
  "default-src": "'self' customprotocol: asset:",
  "connect-src": "ipc: http://ipc.localhost",
  "img-src": "'self' asset: http://asset.localhost blob: data:",
  "style-src": "'unsafe-inline' 'self'"
}
```

> Avoid loading remote content such as scripts served over a CDN. If your frontend uses WebAssembly, include `'wasm-unsafe-eval'` as `script-src`.

## asset-protocol (asset-protocol.mdx)

> Tauri can serve files from disk into the WebView through the **asset** custom protocol (ex `convertFileSrc`). Whether a path is allowed is controlled by **`app.security.assetProtocol`** in `tauri.conf.json`. You must set **`enable`** to `true` and define a **`scope`**.

Forme tableau (allow seul) :

```json
{ "app": { "security": { "assetProtocol": { "enable": true, "scope": ["$APPCACHE/**/*", "$RESOURCE/**/*"] } } } }
```

Forme objet (`allow` + `deny`, `deny` gagne) :

```json
{ "app": { "security": { "assetProtocol": { "enable": true, "scope": { "allow": ["$APPCACHE/**/*"], "deny": ["$APPCACHE/**/secrets/**"] } } } } }
```

> On Unix, `requireLiteralLeadingDot` defaults to `true` : `*`/`**` ne matchent pas les segments à `.` (ex `.cache`). Nommer le segment littéralement ou passer à `false` (élargit l'exposition, à revoir).

## Headers (http-headers.mdx, depuis 2.1.0)

> A header defined in the configuration gets sent along the responses to the webview. This doesn't include IPC messages and error responses.

Noms autorisés : `Access-Control-Allow-*`, `Cross-Origin-Embedder-Policy`, `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`, `Permissions-Policy`, `Service-Worker-Allowed`, `Timing-Allow-Origin`, `X-Content-Type-Options`, `Tauri-Custom-Header` (non prod). CSP définie ailleurs, pas ici.

## Lifecycle / index (lifecycle.mdx, index.mdx)

> The weakest link in your application lifecycle essentially defines your security. Each step can compromise the assumptions and integrity of all subsequent steps.
> Trust boundaries : Rust core (accès complet) vs WebView (accès via IPC/capabilities uniquement). Inspecter toute donnée qui traverse la frontière.

Conduites : tenir Tauri/`rustc`/`nodejs` à jour, auditer dépendances (`npm audit`, `cargo audit`/`vet`/`crev`), ne développer que sur réseau de confiance (dev-server sans mTLS), durcir machines et contrôle d'accès du VCS.
