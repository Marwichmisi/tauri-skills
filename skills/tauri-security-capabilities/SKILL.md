---
name: tauri-security-capabilities
description: Enforce Tauri v2 capabilities, permissions and scopes (CSP, asset-protocol, lifecycle). Use me whenever the agent touches a permission, a capability file, a scope, or a security config — I own the doctrine, plugin fiches only refer to me and never duplicate permissions.
---

# Tauri Security Capabilities

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit valable pour les 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (capability vs permission vs scope vs durcissement).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-capabilities.py` pour valider toute capability.
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Définir une capability (fenêtres/webviews + permissions) | `references/capabilities.md` | `examples/default-capability.json` | `scripts/check-capabilities.py` |
| Définir/étendre une permission ou un scope | `references/permissions.md`, `references/scopes.md` | `examples/permission-toml-example.toml` | `scripts/check-capabilities.py` |
| Durcir CSP / headers / asset-protocol / lifecycle | `references/hardening.md` | `examples/tauri.conf.json` | — (renvoi doc) |
| Choisir permission plugin existante vs écrire une permission | `references/plugin-permissions.md` | `examples/default-capability.json` | `scripts/check-capabilities.py` |
| Doute inter-skill (config schéma, IPC scope côté code, fiche plugin) | voir Frontières | — | — |

## Frontières

- `tauri-plugins-catalogue` : les fiches `plugin/*` (`#permission-table`) ne dupliquent pas la doctrine, elles renvoient ici. Si tu viens d'une fiche plugin, remonte ici pour toute question de permission/scope.
- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet. Ici on ne montre que le snippet `security.capabilities` / `assetProtocol` / `csp`.
- `tauri-ipc-bridge` : scopes côté code (implémentation Rust, `AppManifest::commands`). Ici côté déclaration (capability/permission TOML/JSON).
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucune permission inventée. Format imposé `plugin:scope:cle`, ex `core:window:allow-set-title`, `fs:default`, `core:path:default`.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Voir `examples/default-capability.json` (tiré de `security/capabilities.mdx`) + `examples/tauri.conf.json`.
Valider avec `python3 scripts/check-capabilities.py examples/default-capability.json`.
