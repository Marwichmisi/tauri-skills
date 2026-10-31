# Migration v1 : configuration — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/start/migrate/from-tauri-1.mdx` (titre `Upgrade from Tauri 1.0`, § Summary of Changes / Tauri Configuration, § Environment Variables Changes)

> Below is a summary of the changes from Tauri 1.0 to Tauri 2.0:

## Déplacements `tauri.conf.json` (même fichier, liste exacte)

- `package > productName` and `package > version` moved to top-level object.
- the binary name is no longer renamed to match `productName` automatically, so you must add a `mainBinaryName` string to the top-level object matching `productName`.
- `package` removed.
- `tauri` key renamed to `app`.
- `tauri > allowlist` removed. Refer to [Migrate Permissions](#migrate-permissions).
- `tauri > allowlist > protocol > assetScope` moved to `app > security > assetProtocol > scope`. See [Asset protocol scope](/security/asset-protocol/) for `enable`, glob patterns, `requireLiteralLeadingDot`, and dynamic paths.
- `tauri > cli` moved to `plugins > cli`.
- `tauri > windows > fileDropEnabled` renamed to `app > windows > dragDropEnabled`.
- `tauri > updater > active` removed.
- `tauri > updater > dialog` removed.
- `tauri > updater` moved to `plugins > updater`.
- `bundle > createUpdaterArtifacts` added, must be set when using the app updater.
  - set it to `v1Compatible` when upgrading from v1 apps that were already distributed. See the [updater guide](/plugin/updater/) for more information.
- `tauri > systemTray` renamed to `app > trayIcon`.
- `tauri > pattern` moved to `app > security > pattern`.
- `tauri > bundle` moved top-level.
- `tauri > bundle > identifier` moved to top-level object.
- `tauri > bundle > dmg` moved to `bundle > macOS > dmg`
- `tauri > bundle > deb` moved to `bundle > linux > deb`
- `tauri > bundle > appimage` moved to `bundle > linux > appimage`
- `tauri > bundle > macOS > license` removed, use `bundle > licenseFile` instead.
- `tauri > bundle > windows > wix > license` removed, use `bundle > licenseFile` instead.
- `tauri > bundle > nsis > license` removed, use `bundle > licenseFile` instead.
- `tauri > bundle > windows > webviewFixedRuntimePath` removed, use `bundle > windows > webviewInstallMode` instead.
- `build > withGlobalTauri` moved to `app > withGlobalTauri`.
- `build > distDir` renamed to `frontendDist`.
- `build > devPath` renamed to `devUrl`.

Référence schéma complet : voir skill frère `tauri-config-cli-reference` (généré `reference/config.md`).
Voir `examples/tauri.conf.v1.json` (avant, KO) et `examples/tauri.conf.v2.json` (après, OK).

## Variables d'environnement renommées (même fichier, liste exacte)

> Most of the environment variables read and written by the Tauri CLI were renamed for consistency and prevention of mistakes:

- `TAURI_PRIVATE_KEY` -> `TAURI_SIGNING_PRIVATE_KEY`
- `TAURI_KEY_PASSWORD` -> `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`
- `TAURI_SKIP_DEVSERVER_CHECK` -> `TAURI_CLI_NO_DEV_SERVER_WAIT`
- `TAURI_DEV_SERVER_PORT` -> `TAURI_CLI_PORT`
- `TAURI_PATH_DEPTH` -> `TAURI_CLI_CONFIG_DEPTH`
- `TAURI_FIPS_COMPLIANT` -> `TAURI_BUNDLER_WIX_FIPS_COMPLIANT`
- `TAURI_DEV_WATCHER_IGNORE_FILE` -> `TAURI_CLI_WATCHER_IGNORE_FILENAME`
- `TAURI_TRAY` -> `TAURI_LINUX_AYATANA_APPINDICATOR`
- `TAURI_APPLE_DEVELOPMENT_TEAM` -> `APPLE_DEVELOPMENT_TEAM`
- `TAURI_PLATFORM` -> `TAURI_ENV_PLATFORM`
- `TAURI_ARCH` -> `TAURI_ENV_ARCH`
- `TAURI_FAMILY` -> `TAURI_ENV_FAMILY`
- `TAURI_PLATFORM_VERSION` -> `TAURI_ENV_PLATFORM_VERSION`
- `TAURI_PLATFORM_TYPE` -> `TAURI_ENV_PLATFORM_TYPE`
- `TAURI_DEBUG` -> `TAURI_ENV_DEBUG`

Vérifié par `scripts/check-migrate.py --tauri-conf` (clés v1) et `--text-file` (env v1).
