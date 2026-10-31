# CLI dev + homonymes in-app — extraits doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/reference/_cli.mdx`, titre frontmatter `Command Line Interface`
- `tauri-docs/src/content/docs/reference/_cli_ios.mdx` (sans frontmatter, fragment `### ios`)
- Contraste homonyme : `tauri-docs/src/content/docs/plugin/cli.mdx`, titre `Command Line Interface (CLI)` (fiche catalogue ; doctrine fiche chez `tauri-plugins-catalogue`, permission chez `tauri-security-capabilities`)

## CLI dev — installation (même fichier `_cli.mdx`)

> The Tauri command line interface (CLI) is the way to interact with Tauri throughout the development lifecycle.

```sh
npm install --save-dev @tauri-apps/cli@latest
cargo install tauri-cli --version "^2.0.0" --locked
```

Variantes doc (onglets `CommandTabs`) : npm (`npm run tauri …`), yarn (`yarn tauri …`), pnpm (`pnpm tauri …`), deno (`deno task tauri …`), bun (`bun tauri …`), cargo (`cargo tauri …`).

> For CLI commands related to developing plugins visit the Develop a Tauri Plugin guide (`develop/plugins/`, skill `tauri-plugin-dev`).

## CLI dev — liste des commandes (même fichier)

`## List of Commands` + `$LIST_OF_COMMANDS` : placeholder **généré** (voir `tauri-docs/packages/cli-generator/build.ts`, `pnpm tauri --help` par sous-commande). Le fichier versionné ne liste aucune commande en dur : ne jamais citer de liste inventée, régénérer avant écriture.

Commandes attestées dans le domaine et les frères : `dev`, `build`, `bundle`, `icon`, `init`, `migrate`, `add`, `android`, `ios` (+ `signer`, `plugin`, `help` génériques). Voir `examples/cli-commands.sh`.

## CLI dev — iOS, hôte macOS seul (`_cli_ios.mdx`)

> All iOS commands are only available on macOS hosts.

- `tauri ios` : `init` (Initialize iOS target), `dev` (dev mode + hot-reload Rust, utilise `build.devUrl` + `build.beforeDevCommand`), `build` (release + IPA), `run` (prod). Usage : `tauri ios [OPTIONS] <COMMAND>`, `tauri ios dev [OPTIONS] [DEVICE] [-- <ARGS>...]`.
- `--config <CONFIG>` : JSON strings ou chemins JSON/JSON5/TOML fusionnés avec le fichier défaut, dans l'ordre fourni (le dernier gagne en conflit). Un fichier plateforme (`tauri.{macos,linux,windows,android,ios}.conf.json`) est cherché et fusionné par défaut — usage saveurs (ex beta) identique à `develop/configuration-files.mdx` (skill `tauri-ipc-bridge`).
- Mobile physique : `devUrl` `localhost` remplacé par l'adresse publique automatiquement ; vérifier `TAURI_DEV_HOST` côté framework, `--host`/`--force-ip-prompt`, `--open` (Xcode), `--port` (`TAURI_CLI_PORT`), `--root-certificate-path` (`TAURI_DEV_ROOT_CERTIFICATE_PATH`), `--no-dev-server-wait` (`TAURI_CLI_NO_DEV_SERVER_WAIT`).
- Chaque sous-commande expose `-v/--verbose`, `-h/--help`, `-V/--version`.

## Homonymes — dev CLI vs plugin CLI in-app (ne pas confondre)

| Usage | Commande / config | Lecture matches | Fiche |
|---|---|---|---|
| Dev CLI (cycle dev) | `<pm> tauri dev\|build\|ios …`, `tauri add cli` (installe le plugin) | n/a (process CLI) | ce skill (`reference/_cli*.mdx`) |
| In-app CLI (ton app a une CLI via clap) | `tauri.conf.json > plugins.cli` (`description`, `args[]`, `subcommands{}`) | JS `getMatches()` (`@tauri-apps/plugin-cli`), Rust `app.cli().matches()` (`CliExt`, `tauri_plugin_cli::init()`) | fiche `plugin/cli.mdx` (skill `tauri-plugins-catalogue`) |

> Tauri enables your app to have a CLI through clap. With a simple CLI definition in your `tauri.conf.json` file, you can define your interface and read its argument matches map on JavaScript and/or Rust. (plugin/cli.mdx)

- In-app : installation `tauri add cli` (auto) ou manuelle (`cargo add tauri-plugin-cli`, `lib.rs` `app.handle().plugin(tauri_plugin_cli::init())` sous `#[cfg(desktop)]`, guest bindings `@tauri-apps/plugin-cli`). Détail setup : fiche catalogue.
- In-app : forme `plugins.cli` validée par `scripts/check-config-cli.py --config` (voir `references/config.md`, `examples/tauri.conf.cli.json`).
- In-app : permission `cli:default` en capability (`src-tauri/capabilities/*.json`, `windows: ["main"]`) — doctrine chez `tauri-security-capabilities`, jamais ici.
- Windows prod : pas d'écriture console par défaut (limite OS, voir `tauri#8305` dans la fiche).
- `tauri cli …` comme commande dev **n'existe pas** : rejetée par `scripts/check-config-cli.py --cli`.

Valider avec `python3 scripts/check-config-cli.py --cli examples/cli-commands.sh`.
