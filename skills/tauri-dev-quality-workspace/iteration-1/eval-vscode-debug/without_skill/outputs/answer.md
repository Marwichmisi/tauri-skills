# Debug VS Code — App Tauri v2

## Prérequis
- Extension `CodeLLDB` (`vadimcn.vscode-lldb`) installée.
- Binaire Rust : `src-tauri/target/debug/mon-app` (dev) et `src-tauri/target/release/mon-app` (prod).
- Frontend : `pnpm` (adapter en `yarn` si demandé par la consigne — voir Remarque).

## Fichiers à placer
- `.vscode/launch.json` : voir `launch.json`
- `.vscode/tasks.json` : voir `tasks.json`

## launch.json — 2 configurations

### 1. Dev : `Tauri: dev`
- `type: lldb`, `request: launch`
- `program: ${workspaceFolder}/src-tauri/target/debug/mon-app`
- `cargo.args: ["build", "--manifest-path=${workspaceFolder}/src-tauri/Cargo.toml", "--no-default-features"]`
- `cwd: ${workspaceFolder}`
- `preLaunchTask: ui:dev`

Lance le frontend en background, puis build + debug le binaire dev via LLDB.

### 2. Prod : `Tauri: prod`
- `type: lldb`, `request: launch`
- `program: ${workspaceFolder}/src-tauri/target/release/mon-app`
- `cargo.args: ["build", "--release", "--manifest-path=${workspaceFolder}/src-tauri/Cargo.toml", "--no-default-features"]`
- `preLaunchTask: ui:build`

Build UI prod une fois, puis build Rust `--release` et debug.

## tasks.json — 2 tâches

- `ui:dev` : `yarn dev`, `isBackground: true`, `cwd: ${workspaceFolder}`, problemMatcher background qui se termine sur `Local:\s+http`.
- `ui:build` : `yarn build`, tâche one-shot, problemMatcher `$tsc`.

## Utilisation
1. `Run and Debug > Tauri: dev > Start Debugging (F5)` pour dev.
2. `Run and Debug > Tauri: prod` pour tester le binaire release.
3. Breakpoints Rust + frontend (via navigateur / devtools).

## Remarque pnpm vs yarn
Consigne : app en `pnpm` mais tâches demandées en `yarn dev` / `yarn build`. Fichiers fournis avec `yarn` pour respecter l'éval. En projet réel pnpm, remplacer par :
- `command: pnpm dev` / `pnpm build` ou `command: pnpm`, `args: [dev]` / `[build]`.
