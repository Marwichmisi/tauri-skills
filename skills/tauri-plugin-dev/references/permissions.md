# Permissions de plugin — écrire allow/deny, scopes, sets, default, autogen

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Plugins/index.mdx` (titre `Plugin Development`, section `Command Permissions` et suivantes)

> By default your commands are not accessible by the frontend. If you try to execute one of them, you will get a denied error rejection. To actually expose commands, you also need to define permissions that allow each command.

> See the [Permissions Overview](/security/permissions/) documentation for more information.

## Fichiers (index.mdx)

> Permissions are defined as JSON or TOML files inside the `permissions` directory. Each file can define a list of permissions, a list of permission sets and your plugin's default permission.

## Permissions (index.mdx)

> A permission describes privileges of your plugin commands. It can allow or deny a list of commands and associate command-specific and global scopes.

```toml title="permissions/start-server.toml"
"$schema" = "schemas/schema.json"

[[permission]]
identifier = "allow-start-server"
description = "Enables the start_server command."
commands.allow = ["start_server"]

[[permission]]
identifier = "deny-start-server"
description = "Denies the start_server command."
commands.deny = ["start_server"]
```

Voir `examples/permission-allow-start-server.toml`.
Règle : `identifier` suit la syntaxe identifiant (voir `references/plugin-basics.md`, check `--identifier`) ; `commands.allow`/`commands.deny` = listes snake_case (`start_server`, `upload`, `spawn`), jamais de `plugin:` ici, jamais d'invention.

Check : `python3 scripts/check-plugin-dev.py --permission examples/permission-allow-start-server.toml`.

## Scope (index.mdx)

> Scopes allow your plugin to define deeper restrictions to individual commands. Each permission can define a list of scope objects that define something to be allowed or denied either specific to a command or globally to the plugin.

Struct d'exemple (`src/scope.rs`, `schemars::JsonSchema` requis) :

```rust title="src/scope.rs"
#[derive(Debug, schemars::JsonSchema)]
pub struct Entry {
    pub binary: String,
}
```

### Command Scope (index.mdx)

> Your plugin consumer can define a scope for a specific command in their capability file (see the [documentation](/reference/acl/scope/)). You can read the command-specific scope with the [`tauri::ipc::CommandScope`](https://docs.rs/tauri/2.0.0/tauri/ipc/struct.CommandScope.html) struct.

```rust title="src/commands.rs"
use tauri::ipc::CommandScope;
use crate::scope::Entry;

async fn spawn<R: tauri::Runtime>(app: tauri::AppHandle<R>, command_scope: CommandScope<'_, Entry>) -> Result<()> {
  let allowed = command_scope.allows();
  let denied = command_scope.denies();
  todo!()
}
```

### Global Scope (index.mdx)

> When a permission does not define any commands to be allowed or denied, it's considered a scope permission and it should only define a global scope for your plugin.

```toml title="permissions/spawn-node.toml"
[[permission]]
identifier = "allow-spawn-node"
description = "This scope permits spawning the `node` binary."

[[permission.scope.allow]]
binary = "node"
```

Lecture côté Rust (`GlobalScope`, `docs.rs` linké, jamais copié) :

```rust title="src/commands.rs"
use tauri::ipc::GlobalScope;
use crate::scope::Entry;

async fn spawn<R: tauri::Runtime>(app: tauri::AppHandle<R>, scope: GlobalScope<'_, Entry>) -> Result<()> {
  let allowed = scope.allows();
  let denied = scope.denies();
  todo!()
}
```

> We recommend checking both global and command scopes for flexibility

Voir `examples/permission-scope-spawn-node.toml`.

### Schema (index.mdx)

> The scope entry requires the `schemars` dependency to generate a JSON schema so the plugin consumers know the format of the scope and have autocomplete in their IDEs.

```toml
# we need to add schemars to both dependencies and build-dependencies because the scope.rs module is shared between the app code and build script
[dependencies]
schemars = "0.8"

[build-dependencies]
schemars = "0.8"
```

```rust title="build.rs"
#[path = "src/scope.rs"]
mod scope;

const COMMANDS: &[&str] = &[];

fn main() {
    tauri_plugin::Builder::new(COMMANDS)
        .global_scope_schema(schemars::schema_for!(scope::Entry))
        .build();
}
```

## Permission Sets (index.mdx)

> Permission sets are groups of individual permissions that helps users manage your plugin with a higher level of abstraction. For instance if a single API uses multiple commands or if there's a logical connection between a collection of commands, you should define a set containing them.

```toml title="permissions/websocket.toml"
"$schema" = "schemas/schema.json"
[[set]]
identifier = "allow-websocket"
description = "Allows connecting and sending through a WebSocket"
permissions = ["allow-connect", "allow-send"]
```

Voir `examples/permission-set-websocket.toml`.

## Default Permission (index.mdx)

> The default permission is a special permission set with identifier `default`. It's recommended that you enable required commands by default. For instance the `http` plugin is useless without the `request` command allowed.

```toml title="permissions/default.toml"
"$schema" = "schemas/schema.json"
[default]
description = "Allows making HTTP requests"
permissions = ["allow-request"]
```

Voir `examples/permission-default.toml`.

## Autogenerated Permissions (index.mdx)

> The easiest way to define permissions for each of your commands is to use the autogeneration option defined in your plugin's build script defined in the `build.rs` file. Inside the `COMMANDS` const, define the list of commands in snake_case (should match the command function name) and Tauri will automatically generate an `allow-$commandname` and a `deny-$commandname` permissions.

```rust title="src/commands.rs"
const COMMANDS: &[&str] = &["upload"];

fn main() {
    tauri_plugin::Builder::new(COMMANDS).build();
}
```

Voir `examples/build-rs-autogen.rs`. Commandes en snake_case, match exact du nom de fonction ; permissions générées `allow-<cmd>` / `deny-<cmd>`, jamais inventées à la main.

Frontière : toute question capability/permission côté app (fusion fenêtres, `capabilities/*.json`, `plugin:scope:cle`, `deny` > `allow`) remonte à `tauri-security-capabilities`. Ici côté auteur (fichiers `permissions/*.toml` + `build.rs`).
