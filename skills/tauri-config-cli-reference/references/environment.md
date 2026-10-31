# Variables d'environnement — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/reference/environment-variables.mdx`, titre frontmatter `Environment Variables`
- Complément domaine : `tauri-docs/src/content/docs/reference/_cli_ios.mdx` (`TAURI_DEV_HOST`, `TAURI_DEV_ROOT_CERTIFICATE_PATH`)

> This is a documentation of all environment variables used by tauri core crates and tauri CLI.

## Règle de priorité (même fichier)

> If both environment variable and CLI flag are used, the CLI flag will have priority.

## Entrées de la CLI (même fichier)

- `CI` — CI mode, aucune interaction.
- `TAURI_CLI_CONFIG_DEPTH` — niveaux remontés pour trouver `tauri.conf.json`.
- `TAURI_CLI_PORT` — port du serveur dev intégré (`--port`).
- `TAURI_CLI_WATCHER_IGNORE_FILENAME` — fichier style `.gitignore` surveillé par `dev`.
- `TAURI_CLI_NO_DEV_SERVER_WAIT` — ne pas attendre le frontend (`--no-dev-server-wait`).
- `TAURI_LINUX_AYATANA_APPINDICATOR` — `true`/`1` force `libayatana-appindicator` (tray Linux).
- `TAURI_BUNDLER_WIX_FIPS_COMPLIANT` — option WiX `FipsCompliant`.
- `TAURI_BUNDLER_TOOLS_GITHUB_MIRROR` / `TAURI_BUNDLER_TOOLS_GITHUB_MIRROR_TEMPLATE` — miroir GitHub outillage bundler (ex `https://mirror.example.com/<owner>/<repo>/releases/download/<version>/<asset>`).
- `TAURI_SKIP_SIDECAR_SIGNATURE_CHECK` — saute la vérification de signature des sidecars.
- `TAURI_SIGNING_PRIVATE_KEY` (+ `_PASSWORD`) — clé privée bundles (string ou chemin) ; `TAURI_SIGNING_RPM_KEY` (+ `_PASSPHRASE`) — clé GPG RPM armored.
- `TAURI_WINDOWS_SIGNTOOL_PATH` — chemin `signtool.exe` (Windows).
- `APPLE_CERTIFICATE` (+ `_PASSWORD`, `openssl base64 -A -in …`) — `.p12` code signing ; `APPLE_SIGNING_IDENTITY` — écrase `tauri.conf.json > bundle > macOS > signingIdentity` (déduit de `APPLE_CERTIFICATE` sinon).
- `APPLE_ID` + `APPLE_PASSWORD` + `APPLE_TEAM_ID` (notarisation ; mot de passe app-spécifique ou préfixes `@keychain:`/`@env:`), ou `APPLE_API_KEY` + `APPLE_API_ISSUER` (+ `API_PRIVATE_KEYS_DIR`, `APPLE_API_KEY_PATH`, `.p8` ; **requis pour iOS**).
- `APPLE_PROVIDER_SHORT_NAME` — écrase `bundle > macOS > providerShortName` (multi-teams).
- `APPLE_DEVELOPMENT_TEAM` — écrase `bundle > iOS > developmentTeam`.
- `TAURI_WEBVIEW_AUTOMATION` — automation webview (Linux seul).
- `TAURI_ANDROID_PROJECT_PATH` (`<project>/src-tauri/gen/android`), `TAURI_IOS_PROJECT_PATH` (`<project>/src-tauri/gen/ios`).
- Complément `_cli_ios.mdx` : `TAURI_DEV_HOST` (adresse publique vs `localhost` sur device physique, à lire côté framework), `TAURI_DEV_ROOT_CERTIFICATE_PATH` (`--root-certificate-path`, dev HTTPS mobile).

## Hooks `beforeDevCommand`/`beforeBuildCommand` (même fichier, lecture seule)

> These environment variables are set for each hook command … to conditionally build your frontend.

- `TAURI_ENV_DEBUG` (`true` en `dev`/`build --debug`), `TAURI_ENV_TARGET_TRIPLE`, `TAURI_ENV_ARCH` (`x86_64`, `aarch64`…), `TAURI_ENV_PLATFORM` (`windows`, `darwin`, `linux`…), `TAURI_ENV_PLATFORM_VERSION`, `TAURI_ENV_FAMILY` (`unix`/`windows`).

Toute autre `TAURI_*`/`APPLE_*` est inventée : rejetée par `scripts/check-config-cli.py --env`. Voir `examples/env.sh`.

Valider avec `python3 scripts/check-config-cli.py --env examples/env.sh`.
