# Catalogue — vue d'ensemble (routeur)

Source: `tauri-docs/src/content/docs/plugin/index.mdx`, commit `ec113a50`, titre frontmatter `Features & Recipes`.

> Tauri comes with extensibility in mind. Official Features + Community Resources + Support Table (plateformes par plugin officiel).

## Rôle

Cette fiche est le routeur : elle liste les fonctionnalités officielles et communautaires avec table de compatibilité (`TableCompatibility`, filtres `platformFilters`). Elle ne porte aucune permission ; elle renvoie vers les 29 fiches ci-dessous en une étape de routage.

## Les 29 fiches (hors updater)

autostart, barcode-scanner, biometric, cli, clipboard, deep-linking, dialog, file-system, geolocation, global-shortcut, haptics, http-client, localhost, logging, nfc, notification, opener, os-info, persisted-scope, positioner, process, shell, single-instance, sql, store, stronghold, upload, websocket, window-state.

`plugin/updater.mdx` exclu : vit dans `tauri-distribution` (`references/pipelines-updater.md`).

## Permissions — ne rien inventer

Chaque fiche expose `#default-permission` et `#permission-table`. Toute question de permission/scope/capability se décide dans `tauri-security-capabilities`, pas ici.
