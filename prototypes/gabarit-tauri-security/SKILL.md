---
name: tauri-security-capabilities
description: Enforce Tauri v2 capabilities, permissions and scopes (CSP, asset-protocol, lifecycle). Use me whenever the agent touches a permission, a capability file, a scope, or a security config — I own the doctrine, plugin fiches only refer to me.
---

# Tauri Security Capabilities (prototype — gabarit instancié)

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`. Ne cite rien hors doc locale.
> Gabarit valable pour les 12 skills du pack. Lignes génériques marquées [GABARIT].

## Workflow [GABARIT]

1. Identifier l'intention (capability vs permission vs scope vs CSP/headers).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Si `scripts/` existe pour ce cas, le lancer pour valider (ici `check-capabilities.py`).
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage [GABARIT — adapter par skill]

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Définir une capability (fenêtres/webviews + permissions) | `references/capabilities.md` | `examples/default-capability.json` | `scripts/check-capabilities.py` |
| Définir/étendre une permission ou un scope | `references/permissions.md` | `examples/default-capability.json` | `scripts/check-capabilities.py` |
| Durcir CSP / headers / asset-protocol | `references/capabilities.md` § rappel doc | — (renvoi doc) | — |
| Doute inter-skill (plugin, config, CLI) | voir Frontières | — | — |

## Frontières [GABARIT]

- `tauri-plugins-catalogue` : les fiches plugins (`#permission-table`) ne dupliquent pas la doctrine, elles renvoient ici.
- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet, ici on ne montre que le snippet `security.capabilities`.
- `tauri-ipc-bridge` : scopes de commands côté code, ici côté déclaration capability/permission.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift [GABARIT]

- Extraits `references/` = copie fidèle de `tauri-docs/` avec pointeur `Source:` en tête.
- Aucune permission inventée. Format imposé `plugin:command:scope` type `core:window:allow-set-title`.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Voir `examples/default-capability.json` (tiré de `security/capabilities.mdx`) + `examples/tauri.conf.json`.
Valider avec `python3 scripts/check-capabilities.py examples/default-capability.json`.
