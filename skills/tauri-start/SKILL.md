---
name: tauri-start
description: Start a Tauri v2 project on a supported frontend (Vite, Next, Nuxt, SvelteKit, Qwik, Leptos, Trunk) with prerequisites and correct structure. Use me whenever the agent scaffolds, inits, or configures a frontend, picks frontendDist/devUrl/before commands, or lays out src-tauri/ — I own the start doctrine, config schema details live in tauri-config-cli-reference and security in tauri-security-capabilities.
---

# Tauri Start

> Source-de-vérité : `tauri-docs/` local, commit `ec113a50`, EN canonique seule.
> Ne cite rien hors doc locale. Traductions ignorées. Versions doc : Vite 8, Next.js 14.2.3, Nuxt 4.2, SvelteKit 2.20.4 / Svelte 5.25.8, Trunk 0.17.5, Leptos 0.6.
> Gabarit commun aux 12 skills du pack (voir `docs/gabarit-skill.md`).

## Workflow

1. Identifier l'intention (prérequis vs scaffolder vs structure vs config frontend).
2. Router via le tableau ci-dessous vers la bonne `references/*.md`, la lire.
3. Appliquer l'exemple minimal correspondant de `examples/`.
4. Lancer `scripts/check-start.py` pour valider toute `tauri.conf.json` (frontendDist/devUrl/commandes + `withGlobalTauri` Rust).
5. Renvoyer vers les skills frères si hors périmètre (voir Frontières).

## Routage

| Intention | Lire en premier | Exemple | Script |
|---|---|---|---|
| Vérifier prérequis système/Rust/mobile avant de scaffolder | `references/prerequisites.md` | — (commandes doc) | — |
| Scaffolder via `create-tauri-app` ou `tauri init` manuel | `references/create-project.md` | `examples/project-structure.txt` | `scripts/check-start.py` |
| Poser/contrôler l'arborescence `src-tauri/` | `references/project-structure.md` | `examples/project-structure.txt` | `scripts/check-start.py --project-root` |
| Configurer Vite (recommandé SPA) | `references/frontend-vite.md` | `examples/tauri.conf.vite.json`, `examples/vite.config.example.js` | `scripts/check-start.py --frontend vite` |
| Configurer Next/Nuxt/SvelteKit/Qwik (SSG, pas SSR) | `references/frontend-meta.md` | `examples/tauri.conf.nextjs.json`, `examples/tauri.conf.nuxt.json`, `examples/tauri.conf.sveltekit.json`, `examples/tauri.conf.qwik.json` | `scripts/check-start.py --frontend <nextjs\|nuxt\|sveltekit\|qwik>` (une valeur, `choices`) |
| Configurer Leptos/Trunk (Rust, `withGlobalTauri`, `ws_protocol`) | `references/frontend-rust.md` | `examples/tauri.conf.leptos.json`, `examples/tauri.conf.trunk.json` | `scripts/check-start.py --frontend <leptos\|trunk>` (une valeur) |
| Doute inter-skill (schéma complet, capability, IPC, store) | voir Frontières | — | — |

## Frontières

- `tauri-config-cli-reference` : schéma `tauri.conf.json`/`gen/schemas` complet et CLI (`tauri init/dev/build`, `tauri icon`). Ici on ne montre que le bloc `build` documenté par frontend + `app.withGlobalTauri`.
- `tauri-security-capabilities` : `capabilities/` et permissions/scopes. Ici on ne fait que nommer le dossier, la doctrine vit là-bas.
- `tauri-ipc-bridge` : `develop/` (invoke, sidecar, resources, state). Ici Tauri agit comme hôte statique, pas de serveur.
- `tauri-core-concepts` : architecture, process-model, taille. Ici `start/index.mdx` ne fait que résumer pourquoi Tauri (sécurité, <600KB, flexibilité).
- `tauri-distribution`, `tauri-dev-quality`, `tauri-migrate`, `tauri-plugin-dev`, `tauri-plugins-catalogue`, `tauri-ui-recettes`, `tauri-frontend-bindings` : hors périmètre démarrage ; renvoyer si le besoin réel y bascule.
- Hors pack : `about/`, `contribute`, traductions (EN canonique seule).

## Règle anti-drift

- Extraits `references/` = copies fidèles de `tauri-docs/` avec pointeur `Source:` en tête (fichier + commit + titre frontmatter).
- Aucune valeur inventée. `frontendDist` documentés seuls : `../dist` (Vite/Nuxt/Qwik/Leptos/Trunk), `../out` (Next.js), `../build` (SvelteKit). `devUrl` documentés seuls : `:5173` (Vite/SvelteKit/Qwik), `:3000` (Next/Nuxt), `:1420` (Leptos), `:8080` (Trunk).
- Pas de SSR : SSG/SPA/MPA seuls, `output:'export'` (Next), `ssr:false` (Nuxt/SvelteKit), adapter static (SvelteKit/Qwik). Mobile exige serveur dev joignable sur IP interne.
- `SKILL.md` < 500 lignes ; le détail vit en `references/`, jamais ici.

## Exemple minimal

Voir `examples/tauri.conf.vite.json` (tiré de `start/frontend/vite.mdx`) + `examples/vite.config.example.js` + `examples/project-structure.txt`.
Valider avec `python3 scripts/check-start.py examples/tauri.conf.vite.json --frontend vite`.
