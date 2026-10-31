# IDE Debug — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Debug/vscode.mdx` (titre `Debug in VS Code`)
- `tauri-docs/src/content/docs/develop/Debug/rustrover.mdx` (titre `Debug in JetBrains IDEs`)
- `tauri-docs/src/content/docs/develop/Debug/neovim.mdx` (titre `Debug in Neovim`)

Principe commun (3 fichiers) : on contourne la CLI Tauri (pas de `beforeDevCommand`/`beforeBuildCommand` exécutés). Lancer le serveur dev à part (`preLaunchTask` / Run config / overseer), builder avec Cargo direct + `--no-default-features` pour servir le dev-server au lieu des assets disque.

## VS Code — vscode-lldb, toutes plateformes (vscode.mdx)

Prérequis : extension [`vscode-lldb`].

Voir `examples/launch.json` (copie exacte, 2 configs) + `examples/tasks.json` :

- `Tauri Development Debug` : `type lldb`, `cargo.args` = `build --manifest-path=./src-tauri/Cargo.toml --no-default-features`, `preLaunchTask ui:dev`.
- `Tauri Production Debug` : `type lldb`, `cargo.args` = `build --release --manifest-path=./src-tauri/Cargo.toml`, `preLaunchTask ui:build`.
- `tasks.json` : `ui:dev` (shell `yarn dev`, `isBackground true`), `ui:build` (shell `yarn build`).

Check : `python3 scripts/check-dev-quality.py --vscode examples/launch.json`.

## VS Code — Windows uniquement, cppvsdbg (vscode.mdx)

Prérequis : extension C/C++ + Visual Studio Windows Debugger (plus rapide, meilleur support enums Rust).

- `type cppvsdbg`, `program ${workspaceRoot}/src-tauri/target/debug/your-app-name-here.exe` (adapter le nom, `release/debug` pour prod), `preLaunchTask ui:dev`.
- Groupe `dev` = `build:debug` (type cargo, cwd `src-tauri`) + `ui:dev`, `kind build`, ciblé par `preLaunchTask dev`.

## RustRover / IntelliJ / CLion (rustrover.mdx)

1. Attacher le projet Cargo : `View | Tool Windows | Cargo`, `+ Attach Cargo Project`, choisir `src-tauri/Cargo.toml`. Alternative : workspace racine `[workspace] members = ["src-tauri"]`.
2. Run config Cargo `Run Tauri App` avec `--no-default-features` (la CLI le passe normalement, ici manuel).
3. Run config serveur dev à part : `beforeDevCommand` de `tauri.conf.json` (`pnpm dev` → Run config **npm** avec Command/Scripts/Package Manager ; `trunk serve` → Run config **Shell Script**).
4. Lancer le dev-server, puis Debug sur la config Cargo. Breakpoints Rust reconnus.

## Neovim — nvim-dap + codelldb (neovim.mdx)

Prérequis : binaire `codelldb` (releases `vadimcn/codelldb`), plugins `nvim-dap` + `nvim-dap-ui` (+ `nvim-nio` requis par dap-ui).

Voir `examples/nvim-dap.lua` (copie exacte) : `dap.adapters.codelldb` (`type server`, `command /opt/codelldb/adapter/codelldb`, adapter chemin à adapter), `dap.configurations.rust` (`type codelldb`, `request launch`, `program` = input binaire `target/debug/`, `cwd workspaceFolder`, `stopOnEntry false`).

Serveur dev : plugin `overseer` + `.vscode/tasks.json` type `process` (`trunk serve`, `isBackground true`, problemMatcher `beginsPattern .*Rebuilding.*` / `endsPattern .*server listening at:.*`). Keymaps doc : `F5 continue`, `F6 disconnect`, `F10 step_over`, `F11 step_into`, `F12 step_out`, `Leader b breakpoint`, `Leader o overseer`, `Leader R run_template`.
