# Validation tauri.conf.json in-app — `plugins.cli` (commit ec113a50, EN canonique)

## 1. Config validée (`tauri.conf.json` ci-joint)

Forme in-app seule documentée (`plugin/cli.mdx`, § Base Configuration) :

- `plugins.cli.description` : `"Tauri CLI Plugin Example"` (string non-vide requise).
- `plugins.cli.args[]` : `[{ "short": "v", "name": "verbose", "description": "Verbosity level" }]`
  - Flag : `name` + `short` seul (occurrences comptées) — cf. `references/config.md`.
  - Clés args doc seules : `name/short/description/takesValue/multiple/possibleValues/index` — aucun champ inventé.
- `plugins.cli.subcommands.run` : `{ "description": "Run the application", "args": [{debug}, {release}] }`
  - Même forme que la racine (`description` + `args[]`).
- `$schema` : `"../gen/schemas/desktop-schema.json"` — contient `gen/schemas` (requis par le check).
- Interdit respecté : pas de `cli` à la racine (toujours `plugins.cli`).

Source :
- `references/config.md` → `tauri-docs/src/content/docs/plugin/cli.mdx`, titre `Command Line Interface (CLI)` (§ Base Configuration, Adding Arguments, Subcommands), commit `ec113a50`.
- `$schema` → `tauri-docs/packages/config-generator/build.ts` + `security/capabilities.mdx` (pointeur seul).
- Schéma complet généré `reference/config.md` absent au commit (voir `reference/.gitignore`) : seule la forme `plugins.cli` ci-dessus est citée, le reste renvoie au schéma régénéré.

## 2. CLI dev vs usage in-app — sans erreur d'homonyme (`cli.sh` ci-joint)

| Usage | Commande / config | Lecture matches |
|---|---|---|
| Dev CLI (cycle dev) | `<pm> tauri dev\|build\|ios …`, `tauri add cli` (installe le plugin) | n/a (process CLI) |
| In-app CLI (ton app a une CLI via clap) | `tauri.conf.json > plugins.cli` (`description`, `args[]`, `subcommands{}`) | JS `getMatches()` (`@tauri-apps/plugin-cli`), Rust `app.cli().matches()` (`CliExt`, `tauri_plugin_cli::init()`) |

- Dev : `npm run tauri add cli`, `npm run tauri dev`, `pnpm tauri build`, `pnpm tauri ios init/dev/build` (hôte macOS seul).
- In-app : `getMatches`, `CliExt`, `tauri_plugin_cli::init()`, `plugins.cli`, permission `cli:default`.
- `tauri cli …` comme commande dev **n'existe pas** : rejetée par le check (homonyme).

Source :
- `references/cli.md` → `tauri-docs/src/content/docs/reference/_cli.mdx`, titre `Command Line Interface` (installation, `## List of Commands` + `$LIST_OF_COMMANDS` généré via `packages/cli-generator/build.ts` — jamais cité en dur).
- `tauri-docs/src/content/docs/reference/_cli_ios.mdx` (fragment `### ios` : hôte macOS seul, `--config` merge RFC 7396).
- Contraste homonyme → `tauri-docs/src/content/docs/plugin/cli.mdx`, titre `Command Line Interface (CLI)` : `> Tauri enables your app to have a CLI through clap.`

## 3. Frontières (renvois skills frères)

- `tauri-security-capabilities` : seule autorité capabilities/permissions (`cli:default`, `security.capabilities`, CSP). Ici on ne déclare aucune permission ; la ligne `cli:default` dans `cli.sh` est un pointeur commentaire seul.
- `tauri-plugins-catalogue` : fiche `plugin/cli.mdx` complète (setup `PluginPermissions`, `Compatibility`). Ici contraste homonyme + forme `plugins.cli` seuls.
- `tauri-ipc-bridge` : `develop/configuration-files.mdx` (formats JSON5/TOML, fusion plateforme RFC 7396). Ici `--config` merge seul.
- `tauri-distribution` / `tauri-start` / `tauri-migrate` / `tauri-dev-quality` / `tauri-plugin-dev` : vars signing, `tauri init/dev/build/icon`, `migrate`, debug — hors périmètre, voir skill dédié.

## 4. Validation (commandes)

```sh
python3 skills/tauri-config-cli-reference/scripts/check-config-cli.py --config skills/tauri-config-cli-reference-workspace/iteration-1/eval-config-homonymes/with_skill/outputs/tauri.conf.json
# OK .../tauri.conf.json: JSON valide, plugins.cli conforme (args=1)

python3 skills/tauri-config-cli-reference/scripts/check-config-cli.py --cli skills/tauri-config-cli-reference-workspace/iteration-1/eval-config-homonymes/with_skill/outputs/cli.sh
# OK .../cli.sh: dev=['add', 'build', 'dev', 'ios'], in-app=['CliExt', 'cli:default', 'getMatches', 'plugins\\.cli', 'tauri_plugin_cli']
```

Aucun champ ni commande inventés : clés args et commandes dev limitées aux listes doc ci-dessus.
