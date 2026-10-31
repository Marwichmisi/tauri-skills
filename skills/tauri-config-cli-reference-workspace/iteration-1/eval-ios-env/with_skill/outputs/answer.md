# Build iOS — commandes + env (macOS, device physique, hook)

## Commandes (hôte macOS seul)

Voir `ios-commands.sh` :

```sh
pnpm tauri ios init
CI=true pnpm tauri ios dev --port 1430
pnpm tauri ios build
```

- `ios` : `init` (Initialize iOS target), `dev` (dev mode + hot-reload Rust,
  utilise `build.devUrl` + `build.beforeDevCommand`), `build` (release + IPA).
- Variantes package manager attestées : `pnpm tauri …` (onglets `CommandTabs`).
- `tauri cli …` comme commande dev n'existe pas (homonyme : `tauri add cli`
  installe le plugin, `plugins.cli` le configure).

## Variables (voir `env.conf`)

```conf
CI=true
TAURI_CLI_PORT=1430
TAURI_DEV_HOST=192.168.1.20
# hook lit seulement : $TAURI_ENV_PLATFORM / $TAURI_ENV_DEBUG
```

- `CI` — CI mode, aucune interaction.
- `TAURI_CLI_PORT` — port du serveur dev intégré (`--port`).
- `TAURI_DEV_HOST` — adresse publique vs `localhost` sur device physique,
  à lire côté framework ; `--host` / `--force-ip-prompt` en complément.
- Hook `beforeDevCommand` / `beforeBuildCommand` (lecture seule) :
  `TAURI_ENV_DEBUG` (`true` en `dev` / `build --debug`),
  `TAURI_ENV_PLATFORM` (`darwin` sur macOS) — le hook lit, ne les exporte pas.
- **Règle de priorité : si variable d'environnement et flag CLI coexistent,
  le flag prime** — ex `--port 1430` gagne sur `TAURI_CLI_PORT=1430`.
- Aucune variable inventée : toute autre `TAURI_*` / `APPLE_*` est rejetée
  par `scripts/check-config-cli.py --env`.

## Sources (commit `ec113a50`, EN canonique seule)

- `references/cli.md` ← `tauri-docs/src/content/docs/reference/_cli.mdx`
  (titre `Command Line Interface`) + `reference/_cli_ios.mdx` (fragment `### ios`)
  + contraste `plugin/cli.mdx` (titre `Command Line Interface (CLI)`).
- `references/environment.md` ← `tauri-docs/src/content/docs/reference/environment-variables.mdx`
  (titre `Environment Variables`) + complément `_cli_ios.mdx`
  (`TAURI_DEV_HOST`, `TAURI_DEV_ROOT_CERTIFICATE_PATH`).
- Exemples appliqués : `examples/cli-commands.sh`, `examples/env.sh`.

## Frontières

- Signing/notarisation iOS en contexte release (`APPLE_API_KEY` + `APPLE_API_ISSUER`
  **requis pour iOS**, `APPLE_DEVELOPMENT_TEAM`, `TAURI_IOS_PROJECT_PATH`,
  `TAURI_SIGNING_*`) : usage release → skill `tauri-distribution`.
- Config `tauri.conf.json` / fusion `--config` / plateforme
  (`tauri.ios.conf.json`), formats et merge : skill `tauri-ipc-bridge`.
- Permission in-app `cli:default` / capabilities : skill
  `tauri-security-capabilities`. Fiche setup complet `plugin/cli` :
  skill `tauri-plugins-catalogue`.
- `tauri init/dev/build/icon`, debug/WebDriver : skills `tauri-start`,
  `tauri-dev-quality`.

## Validation

```
OK .../outputs/ios-commands.sh: dev=['ios'], in-app=—
OK .../outputs/env.conf: variables=['CI', 'TAURI_CLI_PORT', 'TAURI_DEV_HOST']
```

Commandes :
`python3 scripts/check-config-cli.py --cli outputs/ios-commands.sh`
`python3 scripts/check-config-cli.py --env outputs/env.conf`
