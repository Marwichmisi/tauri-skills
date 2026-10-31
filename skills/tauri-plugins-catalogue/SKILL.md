---
name: tauri-plugins-catalogue
description: Route to the right Tauri v2 plugin fiche among the 30 (file-system, dialog, shell, store, notification, opener, SQL and 23 more) and wire its setup plus guest-js snippet. Use me whenever the agent picks a plugin, adds it with tauri add, calls its JS API, or references its permissions — I own the one-step catalogue routing, permission doctrine lives in tauri-security-capabilities and updater/auto-update lives in tauri-distribution.
---

# Tauri Plugins Catalogue

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (quel besoin produit → quelle fiche parmi les 30).
2. Router en une étape via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer le snippet fidèle (setup `tauri add` + guest-js/Rust de la fiche, exemples pour fs/dialog/notification).
4. Lancer `scripts/check-catalogue.py --plugin <fiche> [--js <fichier> --capability <capability>]` pour valider routage + permission non inventée.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Vue d'ensemble, chercher une fiche, table compatibilité plateformes | `references/overview.md` | — (routeur) | `scripts/check-catalogue.py --list` |
| Lancer l'app au démarrage système | `references/autostart.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin autostart --capability <cap>` |
| Scanner QR/EAN-13 via caméra (mobile) | `references/barcode-scanner.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin barcode-scanner --capability <cap>` |
| Auth biométrique (Android/iOS) | `references/biometric.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin biometric --capability <cap>` |
| Parser les args CLI in-app (`getMatches`, clap) | `references/cli.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin cli --capability <cap>` |
| Lire/écrire le presse-papiers | `references/clipboard.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin clipboard --capability <cap>` |
| Gérer les deep-links (handler URL) | `references/deep-linking.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin deep-linking --capability <cap>` |
| Dialogues natifs (open/save/message `ask`) | `references/dialog.md` | `examples/dialog.js` + `examples/capability-dialog.json` | `scripts/check-catalogue.py --plugin dialog --js examples/dialog.js --capability examples/capability-dialog.json` |
| Accéder au filesystem (`exists`, `BaseDirectory`) | `references/file-system.md` | `examples/fs.js` + `examples/capability-fs.json` | `scripts/check-catalogue.py --plugin file-system --js examples/fs.js --capability examples/capability-fs.json` |
| Géolocalisation (position, watch) | `references/geolocation.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin geolocation --capability <cap>` |
| Raccourcis globaux (`register`) | `references/global-shortcut.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin global-shortcut --capability <cap>` |
| Haptique/vibration (Android/iOS) | `references/haptics.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin haptics --capability <cap>` |
| Requêtes HTTP (`fetch` Rust) | `references/http-client.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin http-client --capability <cap>` |
| Servir via localhost au lieu du protocole custom | `references/localhost.md` | — (Rust-only, caution doc) | `scripts/check-catalogue.py --plugin localhost --capability <cap>` |
| Logs configurables | `references/logging.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin logging --capability <cap>` |
| Lire/écrire tags NFC (Android/iOS) | `references/nfc.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin nfc --capability <cap>` |
| Notifications natives | `references/notification.md` | `examples/notification.js` + `examples/capability-notification.json` | `scripts/check-catalogue.py --plugin notification --js examples/notification.js --capability examples/capability-notification.json` |
| Ouvrir fichiers/URLs (`openPath`, `openUrl`, reveal) | `references/opener.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin opener --capability <cap>` |
| Info OS (platform, version, arch) | `references/os-info.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin os-info --capability <cap>` |
| Persister les scopes fs/asset à la réouverture | `references/persisted-scope.md` | — (Rust-only) | `scripts/check-catalogue.py --plugin persisted-scope --capability <cap>` |
| Positionner fenêtres (well-known locations) | `references/positioner.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin positioner --capability <cap>` |
| Accéder au process courant (`exit`, `relaunch`) | `references/process.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin process --capability <cap>` |
| Shell/spawn (`Command`, `sidecar`) | `references/shell.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin shell --capability <cap>` |
| Instance unique (`init(\|app, args, cwd\|)`) | `references/single-instance.md` | — (Rust-only) | `scripts/check-catalogue.py --plugin single-instance --capability <cap>` |
| SQL via sqlx (sqlite/mysql/postgres) | `references/sql.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin sql --capability <cap>` |
| Store key-value persistant | `references/store.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin store --capability <cap>` |
| Secrets chiffrés (Stronghold) | `references/stronghold.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin stronghold --capability <cap>` |
| Upload/download HTTP de fichiers | `references/upload.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin upload --capability <cap>` |
| WebSocket (client Rust en JS) | `references/websocket.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin websocket --capability <cap>` |
| Persister taille/position fenêtres | `references/window-state.md` | — (snippet fiche) | `scripts/check-catalogue.py --plugin window-state --capability <cap>` |
| Doute inter-skill (permission/scope, updater, schéma config, code IPC) | voir Frontières | — | — |

## Frontières

- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes (`plugin:scope:cle`, `deny` > `allow`, CSP/asset-protocol). Ici on cite la `#permission-table` de la fiche sans inventer, la doctrine vit là-bas.
- `tauri-distribution` : `plugin/updater.mdx` vit là-bas (`references/pipelines-updater.md`, auto-update/sign/pipelines). Le catalogue = `plugin/**` hors updater (30 fiches) ; toute demande updater part là-bas.
- `tauri-config-cli-reference` : schéma complet `tauri.conf.json`/`gen/schemas`, CLI dev (`tauri init/dev/build/icon`), env-vars. Ici seulement `npm run tauri add <plugin>` + `cargo add tauri-plugin-<nom>` + `.plugin(...::init())`. Homonyme CLI : `getMatches` in-app ici, CLI dev là-bas.
- `tauri-ipc-bridge` : commands/events/state/resources/sidecar côté code. Ici `Command.sidecar`/`resolveResource`/`store` cités sans dupliquer ; le code d'appel part là-bas.
- `tauri-plugin-dev` : création de plugins (scaffold, `permissions/*.toml`, mobile Kotlin/Swift). Ici usage des 30 fiches officielles ; la création part là-bas.
- `tauri-start`, `tauri-migrate`, `tauri-core-concepts`, `tauri-dev-quality`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre catalogue ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucune permission inventée. Préfixes connus seuls (30 + `core:`, voir `scripts/check-catalogue.py --list`) ; `updater:*` rejeté avec renvoi distribution ; forme `plugin:scope:cle` ou set kébab (même `PERM_RE` que le pilote).
- `shell.open` → `opener` (renvoi doc) ; `process` = process courant, spawn dans `shell` ; `localhost` = caution doc (risques sécu) ; `clipboard` préfixe `clipboard-manager`, `file-system` → `fs`, `http-client` → `http`, `logging` → `log`, `os-info` → `os`, `deep-linking` → `deep-link` (frontmatter `plugin:`).
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Dialog : `examples/dialog.js` + `examples/capability-dialog.json` (tirés de `plugin/dialog.mdx`).
Filesystem : `examples/fs.js` + `examples/capability-fs.json` (tirés de `plugin/file-system.mdx`, scope requis sinon `forbidden path`).
Notification : `examples/notification.js` + `examples/capability-notification.json` (tirés de `plugin/notification.mdx`).
Valider avec `python3 scripts/check-catalogue.py --plugin dialog --js examples/dialog.js --capability examples/capability-dialog.json` (idem `file-system`, `notification`) et `python3 scripts/check-catalogue.py --list` (30 fiches).
