# Permissions de plugins — utiliser vs écrire, multi-fenêtres

Sources (commit `ec113a50`) :
- `tauri-docs/src/content/docs/learn/Security/using-plugin-permissions.mdx` (titre `Using Plugin Permissions`)
- `tauri-docs/src/content/docs/learn/Security/writing-plugin-permissions.mdx` (titre `Writing Plugin Permissions`)
- `tauri-docs/src/content/docs/learn/Security/capabilities-for-windows-and-platforms.mdx` (titre `Capabilities for Different Windows and Platforms`)

## Utiliser (using-plugin-permissions.mdx)

> Chaque fiche `plugin/*` expose `#default-permission` et `#permission-table`. Référence-les dans une capability, n'invente jamais de permission. La `default` d'un plugin est auto-ajoutée quand la CLI ajoute le plugin ; pour le reste, ajoute explicitement `plugin:permission` dans `permissions: [...]`.

Si tu hésites entre deux permissions d'une fiche, lis sa `#permission-table` puis remonte ici pour la forme `plugin:scope:cle`.

## Écrire (writing-plugin-permissions.mdx)

> Plugin authors shippe des permissions prédéfinies bien nommées pour chaque commande exposée. Définis `[[permission]]` en TOML avec `commands.allow`/`commands.deny` + `[[permission.scope.allow/deny]]`, regroupe en `[[set]]` (`permissions = [...]`). Les identifiants restent `[a-z]`, max 116.

## Multi-fenêtres / plateformes (capabilities-for-windows-and-platforms.mdx)

> Les capability files ciblent `windows` et/ou `webviews` (globs `*` admis). Deux capabilities qui partagent une fenêtre fusionnent leurs frontières. Décline par fenêtre (`main`, `settings`, `*`) et par plateforme (`platforms = [...]` côté permission, ou capabilities séparées) plutôt qu'une capability globale permissive.

Renvoi : toute question de permission issue du catalogue (`tauri-plugins-catalogue`) se décide ici.
