# Migration bêta 2.0 → stable — extrait doc

Source : `tauri-docs/src/content/docs/start/migrate/from-tauri-2-beta.mdx`, commit `ec113a50`, titre `Upgrade from Tauri 2.0 Beta`.

> This guide walks you through upgrading your Tauri 2.0 beta application to Tauri 2.0 release candidate.

Commande `migrate` identique à v1 (npm/yarn/pnpm/cargo, mêmes onglets) : voir `examples/migrate-commands.sh`. Référence CLI : skill frère `tauri-config-cli-reference`.

## Plugins core : préfixe `core:` (même fichier, § Tauri Core Plugins)

> We changed how Tauri built-in plugins are addressed in the capabilities PR #10390. To migrate from the latest beta version you need to prepend all core permission identifiers in your capabilities with `core:` or switch to the `core:default` permission and remove old core plugin identifiers.

Avant (bêta, KO) — voir `examples/capability-beta.json` :

```json
"permissions": ["path:default", "event:default", "window:default", "app:default", "image:default", "resources:default", "menu:default", "tray:default"]
```

Après (stable, OK) — voir `examples/capability-stable.json` :

```json
"permissions": ["core:path:default", "core:event:default", "core:window:default", "core:app:default", "core:image:default", "core:resources:default", "core:menu:default", "core:tray:default"]
```

Raccourci documenté (même fichier) :

```json
"permissions": ["core:default"]
```

> We also added a new special `core:default` permission set which will contain all default permissions of all core plugins, so you can simplify the permissions boilerplate in your capabilities config.

Vérifié par `scripts/check-migrate.py --capability`. Doctrine permissions/scopes : skill frère `tauri-security-capabilities`.

## Dev server : `TAURI_DEV_HOST` (même fichier, § Built-In Development Server)

> We introduced changes to the network exposure of the built-in development server PR #10437 and PR #10456. The built-in mobile development server no longer exposes network wide and tunnels traffic from the local machine directly to the device.

- iOS physique (direct ou Xcode) : ouvrir Xcode pour établir la connexion macOS↔iOS, puis `tauri ios dev --force-ip-prompt` et choisir l'adresse TUN (finit par `::2`).
- Ne plus tester `TAURI_ENV_PLATFORM` (`android|ios`) pour l'hôte ; tester `TAURI_DEV_HOST` (localhost sauf iOS physique).

Avant (bêta, KO) — voir `examples/vite.config.beta.js` : `internal-ip` + `TAURI_ENV_PLATFORM`.

Après (stable, OK) — voir `examples/vite.config.stable.js` : `const host = process.env.TAURI_DEV_HOST` avec `host || false`, `hmr` conditionnel, port `1430`.

:::note
The `internal-ip` NPM package is no longer required, you can directly use the TAURI_DEV_HOST value instead.
:::

Vérifié par `scripts/check-migrate.py --vite-config`.
