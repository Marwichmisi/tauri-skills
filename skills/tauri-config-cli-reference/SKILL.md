---
name: tauri-config-cli-reference
description: Validate Tauri v2 config and CLIs first time (tauri.conf plugins.cli, dev CLI vs in-app plugin CLI, env-vars, webview versions). Use me whenever the agent validates a config, picks a tauri command, names an env var, or checks a webview — I own the config/CLI/env/webview reference, capability doctrine lives in tauri-security-capabilities and plugin fiches in tauri-plugins-catalogue.
---

# Tauri Config CLI Reference

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée. Références générées (`reference/config.md`, `reference/cli.mdx`, `reference/acl/*.md`) régénérées avant écriture (voir `references/config.md`).
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (config vs dev CLI vs in-app CLI vs env vs webview).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-config-cli.py` (`--config` / `--cli` / `--env`) pour valider tout artefact.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Valider `tauri.conf.json` (`plugins.cli` in-app, `$schema`, fusion `--config`) / consulter ACL générée | `references/config.md` | `examples/tauri.conf.cli.json` | `scripts/check-config-cli.py --config` |
| Choisir la bonne CLI (dev `tauri dev/build/ios` vs in-app `plugins.cli` + `getMatches`/`CliExt`, `tauri add cli`) | `references/cli.md` | `examples/cli-commands.sh` | `scripts/check-config-cli.py --cli` |
| Nommer une variable d'environnement (entrées CLI, priorité flag, hooks `TAURI_ENV_*`) | `references/environment.md` | `examples/env.sh` | `scripts/check-config-cli.py --env` |
| Vérifier une version webview (WebView2 Windows, Android WebView, WebKit macOS/iOS/Linux) | `references/webviews.md` | — (renvoi doc, tables dans le fichier) | — (renvoi doc) |
| Doute inter-skill (capability/permission, fiche plugin, schéma build/bundle complet) | voir Frontières | — | — |

## Frontières

- `tauri-security-capabilities` : seule autorité capabilities/permissions/scopes (`cli:default`, `security.capabilities`, CSP/asset-protocol). Ici on ne déclare aucune permission ; tout `capability`/`allow/deny` remonte là-bas.
- `tauri-plugins-catalogue` : fiches `plugin/*` dont `plugin/cli.mdx` (setup complet in-app, `PluginPermissions`, `Compatibility`). Ici le contraste homonyme + la forme `plugins.cli` seuls.
- `tauri-ipc-bridge` : `develop/configuration-files.mdx` (formats JSON5/TOML, fusion plateforme RFC 7396, `Cargo.toml`/`package.json`), `develop/icons.mdx`, sidecars/resources. Ici `--config` merge + `plugins.cli` seuls.
- `tauri-distribution` : signing/bundler vars d'usage (`TAURI_SIGNING_*`, `APPLE_*`, `WINDOWS_*`) en contexte release, updater/pipelines. Ici la liste env-vars seule.
- `tauri-start`, `tauri-migrate`, `tauri-dev-quality`, `tauri-plugin-dev` : `tauri init/dev/build/icon`, `migrate`, debug/WebDriver, `plugin new`. Ici les commandes attestées seules, le guide prime.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule). Générés absents au commit : régénérer, jamais inventer.

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun contenu inventé. `plugins.cli` sous `plugins` seul (`cli` racine rejeté), clés args doc seules (`name/short/description/takesValue/multiple/possibleValues/index`), `tauri cli` dev rejeté, vars `TAURI_*`/`APPLE_*` doc seules.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Config in-app : `examples/tauri.conf.cli.json` (tiré de `plugin/cli.mdx` Base Configuration).
CLI dev vs in-app : `examples/cli-commands.sh` (tiré de `reference/_cli.mdx` + `reference/_cli_ios.mdx` + `plugin/cli.mdx` Usage).
Env : `examples/env.sh` (tiré de `reference/environment-variables.mdx`).
Valider avec `python3 scripts/check-config-cli.py --config examples/tauri.conf.cli.json`, `--cli examples/cli-commands.sh`, `--env examples/env.sh`.
