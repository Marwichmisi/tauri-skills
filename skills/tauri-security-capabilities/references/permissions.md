# Permissions — extrait doc

Source: `tauri-docs/src/content/docs/security/permissions.mdx`, commit `ec113a50`, titre frontmatter `Permissions`.

> Permissions are descriptions of explicit privileges of commands.
> It can enable commands to be accessible in the frontend of a Tauri application.
> It can map scopes to commands and defines which commands are enabled.
> To grant or deny a permission to your app's window or webview, you must reference the permission in a capability.
> Permissions can be grouped as a set under a new identifier (permission set).

## Identifiant de permission (même fichier)

> - `<name>:default` Indicates the permission is the default for a plugin or application
> - `<name>:<command-name>` Indicates the permission is for an individual command
>
> With **name** we refer to the plugin crate name without the `tauri-plugin-` prefix.
> Identifiers are limited to ASCII lower case alphabetic characters `[a-z]` and max length 116.

Format TOML canonique (même fichier) : voir `examples/permission-toml-example.toml`.

```toml
[[permission]]
identifier = "my-identifier"
description = "This describes the impact and more."
commands.allow = ["read_file"]
```

Arborescence canonique (même fichier) :

```sh
tauri-app
├── src-tauri
│   ├── Cargo.toml
│   ├── permissions
│      └── <identifier>.toml
│   ├── capabilities
│      └── <identifier>.json/.toml
```

> As an application developer the capability files can be written in `json`/`json5` or `toml`, whereas permissions only can be defined in `toml`.

Règle pack (décision #3) : les fiches `plugin/*` (`#permission-table`) renvoient ici, pas de duplication.
