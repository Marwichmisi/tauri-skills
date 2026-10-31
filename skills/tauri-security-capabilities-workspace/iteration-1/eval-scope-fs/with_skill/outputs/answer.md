# Scope fs : lire `$APPLOCALDATA` en bloquant les données webview

## Réponse

Le fichier `scope.toml` (même dossier) définit le scope demandé en
réutilisant uniquement les identifiants fs documentés, regroupés en
deux sets réutilisables :

- `scope-applocaldata-recursive` — `[[permission.scope.allow]]` avec
  `path = "$APPLOCALDATA/**"` (accès récursif complet).
- `deny-webview-data-linux` (`platforms = ["linux"]`,
  deny `path = "$APPLOCALDATA/**"`) et `deny-webview-data-windows`
  (`platforms = ["windows"]`, deny `path = "$APPLOCALDATA/EBWebView/**"`).
- Set `deny-default` = `["deny-webview-data-linux", "deny-webview-data-windows"]`.
- Set `scope-applocaldata-reasonable` =
  `["scope-applocaldata-recursive", "deny-default"]` : c'est le set à
  référencer pour obtenir « lecture `$APPLOCALDATA` sauf données webview ».

## Pourquoi c'est sûr : deny gagne sur allow

Règle canonique (même fichier doc) :

> Scopes are categorized into `allow` or `deny` scopes, where `deny`
> always supersedes the `allow` scope.

Concrètement : même si `$APPLOCALDATA/**` est autorisé en lecture, tout
chemin couvert par un scope `deny` reste interdit. Sur Windows,
`$APPLOCALDATA/EBWebView/**` (données et configuration de la webview)
reste donc bloqué malgré l'allow récursif ; sur Linux, l'intégralité de
`$APPLOCALDATA` est refusée car c'est là que sont stockées les données
webview. La doc précise que permettre cet accès « can lead to sensitive
information disclosure and should be well considered ».

## Usage

Ces scopes s'utilisent soit pour toutes les commandes (scope global du
plugin), soit combinés à une commande activée dans une permission
(p. ex. avec `allow-read-file` dans un set `read-files-applocaldata`,
exemple donné par la doc). Pour activer le set dans l'app, le
référencer depuis une capability (`src-tauri/capabilities/`) — voir le
skill `tauri-security-capabilities`, `references/capabilities.md`.

## Sources

- `tauri-docs/src/content/docs/security/scope.mdx`, commit `ec113a50`,
  titre frontmatter `Command Scopes` (canonique EN seule — règle du skill).
- Extraits fidèles relayés par le skill : `references/scopes.md`.
- Aucune permission inventée : `scope-applocaldata-recursive`,
  `deny-webview-data-linux`, `deny-webview-data-windows`, `deny-default`,
  `scope-applocaldata-reasonable` existent tous verbatim dans ce fichier
  doc au commit `ec113a50`.
