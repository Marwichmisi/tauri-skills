# Sidecar — extrait doc (doublon Node regroupe)

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/sidecar.mdx` (titre `Embedding External Binaries`)
- `tauri-docs/src/content/docs/learn/sidecar-nodejs.mdx` (titre `Node.js as a sidecar`)

> We recommend reading the general sidecar guide first for a deeper understanding of how Tauri sidecars work. (sidecar-nodejs.mdx)

## Declarer (sidecar.mdx)

> You may need to embed external binaries ... We call this binary a `sidecar`. To bundle the binaries ... add the `externalBin` property to the `bundle` object in your `tauri.conf.json`.

Voir `examples/tauri.conf.sidecar.json` :

```json { "bundle": { "externalBin": ["/absolute/path/to/sidecar", "../relative/path/to/binary", "binaries/my-sidecar"] } }
```

> The relative paths are relative to the `tauri.conf.json` file which is in the `src-tauri` directory. So `binaries/my-sidecar` would represent `<PROJECT ROOT>/src-tauri/binaries/my-sidecar`.

> To make the external binary work on each supported architecture, a binary with the same name and a `-$TARGET_TRIPLE` suffix must exist on the specified path. For instance, `"externalBin": ["binaries/my-sidecar"]` requires a `src-tauri/binaries/my-sidecar-x86_64-unknown-linux-gnu` executable on Linux or `src-tauri/binaries/my-sidecar-aarch64-apple-darwin` on Mac OS with Apple Silicon.

Triple courant : `rustc --print host-tuple` (Rust 1.84+ ; sinon parser `rustc -Vv`). Rename : voir `examples/sidecar-rename.js` (meme script dans les deux fichiers doc, `fs.renameSync` + `execSync`, `.exe` sur win32, `src-tauri/binaries/sidecar-<triple>`).

## Executer Rust (sidecar.mdx)

> Please follow the shell plugin guide first to set up and initialize the plugin correctly. Without the plugin being initialized and configured the example won't work.

```rust
use tauri_plugin_shell::ShellExt;
let sidecar_command = app.shell().sidecar("my-sidecar").unwrap();
let (mut rx, mut child) = sidecar_command.spawn().expect("Failed to spawn sidecar");
// rx.recv() -> CommandEvent::Stdout, app.emit(...), child.write(...)
```

> The `sidecar()` function expects just the filename, NOT the whole path configured in the `externalBin` array. Ex `externalBin: ["binaries/app", "my-sidecar"]` -> `sidecar("app")` / `sidecar("my-sidecar")`, jamais `sidecar("binaries/app")`.

## Executer JS (sidecar.mdx)

> In the JavaScript code, import the `Command` class from the `@tauri-apps/plugin-shell` module and use the `sidecar` static method. `Command.sidecar('binaries/my-sidecar')`.

> The string provided to `Command.sidecar` must match one of the strings defined in the `externalBin` configuration array.

Permissions (renvoi securite, meme fichier) : `shell:allow-execute` (ou `shell:allow-spawn` pour `spawn()`) avec `{ name: "binaries/app", sidecar: true }` dans `capabilities/default.json`. Args : `true` (tout), `false` (rien), ou liste ordonnee exacte (statiques + `{ validator: "\\S+" }`) ; appel Rust `.args([...])` / JS `Command.sidecar(name, [...])` avec EXACTEMENT l'ordre declare.

## Doublon Node (sidecar-nodejs.mdx, desktop only)

Buts : packager une app Node en binaire autonome (`pkg`, ici `@yao-pkg/pkg`) pour ne pas exiger Node chez l'utilisateur ; alternative : embarquer le runtime + JS en `resources` (lisible, plus lourd). IPC : `process.argv` / `console.log`, ou localhost/stdin/sockets (avantages/inconvenients/securite a peser).

Guide (6 etapes, meme fichier) : `sidecar-app/` a la racine Tauri + `pkg` en dev-dep ; `index.js` (`process.argv[2]` switch `hello`, `console.log`, `process.exit(1)`) ; `package.json` script `pkg index.ts --output my-sidecar` ; `rename.js` vers `../src-tauri/binaries/my-sidecar-<triple>` ; capability `shell:allow-execute` (`args: true`, `name: binaries/my-sidecar`, `sidecar: true`) ; `bundle.externalBin: ["binaries/my-sidecar"]`.

Execution Node (meme fichier) : JS `Command.sidecar('binaries/my-sidecar', ['hello', message]).execute()` -> `output.stdout` ; Rust `#[tauri::command] async fn hello(app, cmd, message)` + `.arg(cmd).arg(message)` + `.output().await` + `invoke("hello", { cmd: 'hello', message })`.

Lien `bundle > externalBin` : voir reference config. Plugin `shell` : voir catalogue (doctrine permissions ici seulement citee, jamais dupliquee).
