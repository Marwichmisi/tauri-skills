---
name: tauri-core-concepts
description: Explain and apply Tauri v2 core concepts before coding (architecture, process model, IPC patterns brownfield/isolation, app size). Use me whenever the agent must justify a design choice — where logic lives, events vs commands, which IPC pattern, how to keep the app small. I own the design doctrine; permissions go to tauri-security-capabilities, command/event code to tauri-ipc-bridge, config schema to tauri-config-cli-reference.
---

# Tauri Core Concepts

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. API Rust linkée, jamais copiée.
> Gabarit valable pour les 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention de conception (architecture vs process-model vs IPC pattern vs taille).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Justifier le choix en citant la source (`concept/**`, commit `ec113a50`) — pas de `scripts/` (exemption `docs/gabarit-skill.md` : scripts UNIQUEMENT si besoin réel ; ici guidance documentaire, aucun format mécanique à valider).
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Expliquer l'architecture (ce que Tauri est / n'est pas, crates core, tooling, TAO/WRY, plugins) | `references/architecture.md` | — (renvoi doc, pas de snippet config) | — (documentaire, pas de `scripts/`) |
| Placer la logique (Core Rust vs Webview frontend, least-privilege, état global) | `references/process-model.md` | — (décision documentaire) | — (documentaire, pas de `scripts/`) |
| Choisir Events vs Commands, brownfield vs isolation, écrire le hook et la config `pattern` | `references/ipc-patterns.md` | `examples/brownfield-pattern.json`, `examples/isolation-pattern.json`, `examples/isolation-hook.js` | — (documentaire, pas de `scripts/`) |
| Réduire la taille (profil Cargo stable/nightly, `removeUnusedCommands`) | `references/app-size.md` | `examples/cargo-size-profile.toml`, `examples/remove-unused-commands.json` | — (documentaire, pas de `scripts/`) |
| Doute inter-skill (permission/scope, code command/event, schéma config complet) | voir Frontières | — | — |

## Frontières

- `tauri-security-capabilities` : seule autorité sur capabilities, permissions, scopes, CSP, asset-protocol, lifecycle. Ici on ne déclare aucune permission ; tout `plugin:…` ou `capability` remonte là-bas.
- `tauri-ipc-bridge` : implémentation côté code des commands, events, state, resources, sidecar. Ici côté conception (quand utiliser Events vs Commands, quel pattern) ; le code d'appel part là-bas.
- `tauri-config-cli-reference` : schéma complet `tauri.conf.json` / `gen/schemas`, env-vars, webviews. Ici on ne montre que les snippets `app.security.pattern` et `build.removeUnusedCommands`.
- `tauri-start` / `tauri-migrate` : scaffolding frontend et migration v1. Ici on suppose le projet existant.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucun contenu inventé. Pas de permission, de config ou de chiffre de taille inventé.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Choix brownfield (défaut, voir `references/ipc-patterns.md`) : `examples/brownfield-pattern.json` (forme explicite ; le pattern étant défaut, aucune option n'est requise).
Choix isolation + hook : `examples/isolation-pattern.json` + `examples/isolation-hook.js`.
Taille : `examples/cargo-size-profile.toml` (stable) + `examples/remove-unused-commands.json` (nécessite `tauri@2.4`, voir référence).
Validation : pas de `scripts/` (exemption gabarit) — vérifier que chaque choix cite sa source `concept/**` commit `ec113a50` et qu'aucun contenu n'est inventé.
