# Config, dev, icones — extrait doc

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/configuration-files.mdx` (titre `Configuration Files`)
- `tauri-docs/src/content/docs/develop/icons.mdx` (titre `App Icons`)
- `tauri-docs/src/content/docs/develop/index.mdx` (titre `Develop`)

## Fichiers (configuration-files.mdx)

> Since Tauri is a toolkit for building applications there can be many files to configure project settings. Some common files : `tauri.conf.json`, `package.json` and `Cargo.toml`.

Tauri config : source de la webapp, metadata, bundles, plugins, runtime (windows, tray, menus). Voir `examples/tauri.conf.dev.json` + `references/resources.md` + `references/sidecar.md` pour `bundle`. Ref complete : skill frere `tauri-config-cli-reference`.

Formats : JSON defaut ; JSON5/TOML via feature `config-json5`/`config-toml` sur `tauri` + `tauri-build` (noms kebab en TOML, sensible a la casse). Plateformes : `tauri.{linux,windows,macos,android,ios}.conf.json` fusionne via JSON Merge Patch RFC 7396 — les objets fusionnent, les tableaux (dont `bundle.resources`, `app.windows`) sont REMPLACES entierement (tout repeter). `--config` CLI (raw JSON ou fichier) : meme merge, ex `tauri.beta.conf.json` (`productName`, `identifier` beta).

`Cargo.toml` (meme fichier) : `tauri-build` + `tauri` meme mineur que la CLI, `serde`/`serde_json`, `features=[]` auto-gere par `tauri dev/build`, `Cargo.lock` a commiter, jamais `src-tauri/target`.

`package.json` (meme fichier) : scripts `dev`/`build` + `tauri`, deps `@tauri-apps/api` + `@tauri-apps/cli`, branchement via `build.beforeDevCommand`/`beforeBuildCommand` ; lockfile a commiter.

## Dev (index.mdx)

Voir `examples/tauri.conf.dev.json` : `build.devUrl` + `beforeDevCommand`, ou `frontendDist: ./src` (avec `index.html`) sans bundler.

> The built-in Tauri development server does not support mutual authentication or encryption. You should never use it for untrusted networks. (voir `security/lifecycle.md` -> skill securite).

Desktop : `tauri dev` (premier build Rust long, cache ensuite ; clic-droit Inspect). Mobile : `tauri android|ios dev`, `TAURI_DEV_HOST` (Vite `host/process.env`, `strictPort`, `hmr ws`), `--open` (IDE, process CLI vivant requis), inspecteurs Safari/Chrome, `.taurignore` (gitignore-like), `tauri-invoke-http` pour navigateur (APIs inop hors webview), committer `Cargo.lock`, jamais `target/`.

## Icones (icons.mdx)

> Tauri ships with a default iconset ... This is NOT what you want when you ship your application. `icon` command : input `./app-icon.png` (PNG carre ou SVG + transparence) -> toutes plateformes. Desktop en `src-tauri/icons` (inclus auto) ; mobile injecte Xcode/Android Studio.

Voir `examples/bundle-icon.json` (desktop) : `bundle.icon` (`32x32.png`, `128x128.png`, `128x128@2x.png`, `icon.icns`, `icon.ico`). Types : `icns` macOS, `ico` Windows (couches 16..256, 32px en premier en dev), `png` Linux (carre, RGBA, 32bit ; 32/128/256/512, a minima sortie `tauri icon`). Manuel : respecter couches `icns` (repo Tauri), `ico` 16-256, Android `mipmap-*/ic_launcher*` + foreground, iOS `AppIcon.appiconset` sans transparence (20/29/40 1x2x3x+extra, 60 2x3x, 76 1x2x, 83.5 2x, 512 2x).

Schema complet + CLI `tauri icon` : skill frere `tauri-config-cli-reference`. Securite (CSP/asset-protocol/lifecycle) : skill frere `tauri-security-capabilities`.
