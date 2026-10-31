# Validation tauri.conf.json in-app CLI — homonymes `cli`

## 1. Config validée (`tauri.conf.json`)

Le bloc in-app est sous `plugins.cli` (plugin `@tauri-apps/plugin-cli` / `tauri-plugin-cli`), pas la config de la CLI dev :

```json
{
  "$schema": "../gen/schemas/config-schema.json",
  "plugins": {
    "cli": {
      "description": "Demo app showcasing in-app CLI (verbose + run subcommand)",
      "args": [
        {
          "name": "verbose",
          "short": "v",
          "takes_value": false,
          "description": "Enable verbose output"
        }
      ],
      "subcommands": {
        "run": {
          "description": "Run in a given mode",
          "args": [
            { "name": "debug", "takes_value": false, "description": "Run in debug mode" },
            { "name": "release", "takes_value": false, "description": "Run in release mode" }
          ]
        }
      }
    }
  }
}
```

Points validés :
- `description` au niveau `plugins.cli` + au niveau subcommand `run` : requis pour l'aide générée (`--help`).
- `args.verbose` : `name: "verbose"`, `short: "v"` (donc `-v` / `--verbose`), `takes_value: false` = flag booléen.
- `subcommands.run` avec `args: debug / release` : `myapp run --debug` ou `myapp run --release`.
- `$schema: "../gen/schemas/config-schema.json"` : chemin relatif depuis `src-tauri/tauri.conf.json` vers `src-tauri/gen/schemas/config-schema.json`, généré par `tauri dev/build` ou `tauri info`. Active l'autocomplétion/validation dans l'éditeur.

Validation : `jq` + test du schéma, voir `cli.sh`.

## 2. Homonymes — ne pas confondre (sans erreur)

| | CLI dev (outillage) | CLI in-app (runtime) |
|---|---|---|
| Quoi | Binaire `tauri` / `cargo tauri` : scaffolding, dev, build | Args de **ton app compilée** parsés au runtime |
| Install | `npm i -D @tauri-apps/cli` puis `tauri add cli` (ajoute dep + config + permissions) | `npm i @tauri-apps/plugin-cli` (frontend) + `tauri-plugin-cli` (Rust) |
| Commandes | `tauri dev`, `tauri build`, `tauri info`, `tauri add cli` | `myapp --verbose`, `myapp run --debug`, `myapp -v run --release` |
| Code | Jamais dans le code app | Rust : `app.cli().get_matches()` / trait `CliExt` ; JS : `import { getMatches } from '@tauri-apps/plugin-cli'` |
| Permissions | N/A | Requis : `cli:default` (ou `cli:allow-get-matches`) dans `src-tauri/capabilities/*.json`, sinon `getMatches()` échoue |

Règle : `tauri dev/build` lit `tauri.conf.json` pour compiler ; `getMatches()/CliExt` lit `plugins.cli` **à l'exécution** de l'app produite.

## 3. Usage in-app minimal

Rust (`src-tauri/src/lib.rs`) :
```rust
use tauri_plugin_cli::CliExt;
let matches = app.cli().get_matches()?;
let verbose = matches.args.get("verbose").map(|a| a.value.as_bool().unwrap_or(false)).unwrap_or(false);
if let Some(run) = matches.subcommands.get("run") {
  let debug = run.args.get("debug").map(|a| a.value.as_bool().unwrap_or(false)).unwrap_or(false);
}
```

JS :
```js
import { getMatches } from '@tauri-apps/plugin-cli';
const m = await getMatches();
const verbose = m.args.verbose?.value === true;
```

Capabilities (`src-tauri/capabilities/default.json`) :
```json
{ "permissions": ["cli:default"] }
```

## 4. Test

```sh
./cli.sh
myapp --help
myapp -v run --debug
myapp run --release
```
