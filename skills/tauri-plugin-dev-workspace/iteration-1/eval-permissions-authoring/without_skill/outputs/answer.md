# Permissions plugin `my-plugin` — commande `upload`

Artefacts : `artefacts/permissions/`, `artefacts/src/scope.rs`, `artefacts/build.rs`, `artefacts/Cargo.toml.snippet`.

## 1. allow-upload / deny-upload (`commands.allow` / `deny`, snake_case)

`artefacts/permissions/upload.toml` :

```toml
"$schema" = "schemas/schema.json"

[[permission]]
identifier = "allow-upload"
description = "Enables the upload command."
commands.allow = ["upload"]

[[permission]]
identifier = "deny-upload"
description = "Denies the upload command."
commands.deny = ["upload"]
```

Commande en snake_case (`upload`) comme exigé pour `COMMANDS`.

## 2. Scope global `allow-spawn-node` (binary `node`)

`artefacts/permissions/spawn-node.toml` (permission scope : pas de `commands`, uniquement `scope`) :

```toml
"$schema" = "schemas/schema.json"

[[permission]]
identifier = "allow-spawn-node"
description = "This scope permits spawning the `node` binary."

[[permission.scope.allow]]
binary = "node"
```

`artefacts/src/scope.rs` :

```rust
#[derive(Debug, schemars::JsonSchema)]
pub struct Entry {
    pub binary: String,
}
```

Lecture côté commande via `tauri::ipc::GlobalScope<'_, Entry>` (`scope.allows()` / `scope.denies()`).

Dépendance `schemars` en `[dependencies]` ET `[build-dependencies]` (module partagé app + build), voir `artefacts/Cargo.toml.snippet`.

## 3. Set `allow-websocket`

`artefacts/permissions/websocket.toml` :

```toml
"$schema" = "schemas/schema.json"

[[set]]
identifier = "allow-websocket"
description = "Allows connecting and sending messages through a WebSocket"
permissions = ["allow-connect", "allow-send"]
```

## 4. Default `allow-request`

`artefacts/permissions/default.toml` :

```toml
"$schema" = "schemas/schema.json"

[default]
description = "Allows making HTTP requests"
permissions = ["allow-request"]
```

## 5. build.rs — `COMMANDS = ["upload"]` + autogen + `global_scope_schema`

`artefacts/build.rs` :

```rust
#[path = "src/scope.rs"]
mod scope;

const COMMANDS: &[&str] = &["upload"];

fn main() {
    tauri_plugin::Builder::new(COMMANDS)
        .global_scope_schema(schemars::schema_for!(scope::Entry))
        .build();
}
```

`COMMANDS = ["upload"]` génère automatiquement `allow-upload` / `deny-upload`.

## 6. Validation

Demandé : `scripts/check-plugin-dev.py --permission` sans identifiant inventé.

Résultat honnête : `scripts/check-plugin-dev.py` n'existe pas dans ce repo (`scripts/` ne contient que `check-tracabilite.py`). Validation impossible via ce script — non exécuté, non contourné.

Contrôle manuel effectué à la place (TOML parsé, voir transcript) :
- Tous les fichiers parsent en TOML.
- Identifiants strictement limités au périmètre demandé : `allow-upload`, `deny-upload`, `allow-spawn-node`, `allow-websocket` (+ refs `allow-connect`, `allow-send`), `default` (+ ref `allow-request`). Aucun identifiant inventé.
- `COMMANDS` contient bien `"upload"` ; `global_scope_schema(schemars::schema_for!(scope::Entry))` présent.

## 7. Rappel capability côté app

La capability côté application (fichier `capabilities/*.json`, `permissions` + `windows` + `identifier`) ne vit pas ici : elle relève de `tauri-security-capabilities`. Ce plugin n'expose que permissions / sets / scopes ; l'activation effective (`my-plugin:allow-upload`, `my-plugin:allow-spawn-node` avec `scope.allow: [{binary: "node"}]`, etc.) se fait dans la capability de l'app.
