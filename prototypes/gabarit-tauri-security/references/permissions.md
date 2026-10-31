# Permissions — extrait doc (prototype)

Source: `tauri-docs/src/content/docs/security/permissions.mdx`, commit `ec113a50`, titre frontmatter `Permissions`.

> Permissions are descriptions of explicit privileges of commands.
> It can enable commands to be accessible in the frontend of a Tauri application.
> It can map scopes to commands and defines which commands are enabled.
> To grant or deny a permission to your app's window or webview, you must reference the permission in a capability.
> Permissions can be grouped as a set under a new identifier (permission set).

Format TOML canonique (même fichier) :

```toml
[[permission]]
identifier = "my-identifier"
description = "This describes the impact and more."
commands.allow = ["read_file"]
```

Règle pack (cf. décision découpage) : les fiches `plugin/*` (`#permission-table`) renvoient ici, pas de duplication.
