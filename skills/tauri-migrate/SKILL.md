---
name: tauri-migrate
description: Migrate a Tauri v1 app to v2 and beta to stable step by step (config moves, mobile lib, plugin swaps, core: prefix, TAURI_DEV_HOST, dep sync). Use me whenever the agent migrates, upgrades, or syncs Tauri deps — I own the migration path, schema details live in tauri-config-cli-reference, permission doctrine in tauri-security-capabilities, IPC and plugin code in tauri-ipc-bridge and tauri-plugins-catalogue.
---

# Tauri Migrate

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (conf v1→v2 vs code Rust/JS vs bêta→stable vs sync deps).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/` (avant/KO vs après/OK).
4. Lancer `scripts/check-migrate.py` avec les fichiers migrés pour valider chaque artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Migrer `tauri.conf.json` v1→v2 (clés, allowlist, updater, env) | `references/from-v1-config.md` | `examples/tauri.conf.v2.json` (KO : `examples/tauri.conf.v1.json`) | `scripts/check-migrate.py --tauri-conf` (`--text-file` pour env) |
| Migrer code Rust/JS + lib mobile (plugins, menu/tray/path, events) | `references/from-v1-code.md` | `examples/main.v2.js`, `examples/Cargo.v2-mobile.toml`, `examples/migrate-commands.sh` | `scripts/check-migrate.py --js-entry --rust-src --cargo-toml --mobile --package-json` |
| Migrer bêta→stable (`core:`, dev server `TAURI_DEV_HOST`) | `references/from-beta.md` | `examples/capability-stable.json`, `examples/vite.config.stable.js` | `scripts/check-migrate.py --capability --vite-config` |
| Synchroniser deps npm/cargo (même mineure, patch exact plugins) | `references/updating-dependencies.md` | `examples/updating-deps.sh`, `examples/package.v2.json` | `scripts/check-migrate.py --package-json --cargo-toml` |
| Doute inter-skill (schéma complet, capability, IPC, fiche plugin) | voir Frontières | — | — |

## Frontières

- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet et CLI (`migrate`, `init`, `dev`, `build`, `icon`, env-vars, webviews). Ici on ne montre que les renommages v1→v2 et la commande `migrate` (le guide prime sur la commande).
- `tauri-security-capabilities` : capabilities/permissions/scopes et durcissement (CSP, asset-protocol, lifecycle). Ici on ne fait que nommer `capabilities/` et le préfixe `core:` bêta→stable, la doctrine vit là-bas.
- `tauri-ipc-bridge` : scopes côté code (`AppManifest::commands`), invoke/sidecar/resources/state. Ici côté migration des appels (`api::` → plugins), le détail IPC vit là-bas.
- `tauri-plugins-catalogue` : les 30 fiches `plugin/*` (updater, shell, fs…). Ici on ne fait que pointer le plugin de remplacement, la fiche vit là-bas.
- `tauri-start`, `tauri-core-concepts`, `tauri-dev-quality`, `tauri-plugin-dev`, `tauri-distribution`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre migration ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucune valeur inventée. Migrations documentées seules : clés listées en `from-v1-config.md`, plugins `tauri-plugin-* = "2"` + `@tauri-apps/plugin-* ^2.0.0`, `core:default` ou `core:<plugin>:default`, `TAURI_DEV_HOST` (pas `internal-ip`), env renommées listées.
- La commande `migrate` n'est jamais un substitut au guide (danger doc) ; l'ordre pas-à-pas se vérifie dans la réponse, pas seulement dans le script.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Voir `examples/tauri.conf.v2.json` (après, tiré de `start/migrate/from-tauri-1.mdx`) + `examples/main.v2.js` + `examples/capability-stable.json`.
Valider avec `python3 scripts/check-migrate.py --tauri-conf examples/tauri.conf.v2.json --js-entry examples/main.v2.js --capability examples/capability-stable.json --vite-config examples/vite.config.stable.js`.
