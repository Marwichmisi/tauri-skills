# Créer un projet — extrait doc

Source : `tauri-docs/src/content/docs/start/create-project.mdx`, commit `ec113a50`, titre `Create a Project`.

> One thing that makes Tauri so flexible is its ability to work with virtually any frontend framework. We've created the [`create-tauri-app`](https://github.com/tauri-apps/create-tauri-app) utility to help you create a new Tauri project using one of the officially maintained framework templates.

Templates officiels (même fichier) : vanilla (HTML/CSS/JS sans framework), Vue.js, Svelte, React, SolidJS, Angular, Preact, Yew, Leptos, Sycamore. Autres : Awesome Tauri.

## Via `create-tauri-app` (recommandé pour démarrer)

> To get started using `create-tauri-app` run one of the below commands in the folder you'd like to setup your project.

Suivre les invites : nom projet, identifiant (`com.tauri-app.app`), langage frontend (`TypeScript / JavaScript` | `Rust (cargo)` | `.NET (dotnet)`), package manager (pnpm/yarn/npm/bun), UI template + flavor.

Conseil doc (même fichier) si hésitation : `TypeScript / JavaScript` + `pnpm` + `Vanilla` + `TypeScript`. On peut intégrer un framework plus tard (`start/frontend/`).

Démarrage dev (même fichier, Tauri CLI) :

```sh
cd tauri-app
pnpm install
pnpm tauri dev
```

Variantes npm/yarn/deno/bun/cargo documentées (cargo : `cargo install tauri-cli --version "^2.0.0" --locked` puis `cargo tauri dev`).

## Setup manuel (Tauri CLI, frontend existant)

> If you already have an existing frontend or prefer to set it up yourself, you can use the Tauri CLI to initialize the backend for your project separately.

1. Initialiser le frontend (ex Vite) :
   `pnpm create vite .` (variantes npm/yarn/deno/bun documentées).
2. Installer la CLI : `pnpm add -D @tauri-apps/cli@latest` (variantes npm/yarn/deno/bun/cargo documentées).
3. Noter l'URL du serveur dev frontend (ex Vite `http://localhost:5173`).
4. Initialiser : `pnpm tauri init`, puis répondre :
   ```
   ✔ What is your app name? tauri-app
   ✔ What should the window title be? tauri-app
   ✔ Where are your web assets located? ..
   ✔ What is the url of your dev server? http://localhost:5173
   ✔ What is your frontend dev command? pnpm run dev
   ✔ What is your frontend build command? pnpm run build
   ```
   Crée `src-tauri/` avec les fichiers de config nécessaires.
5. Vite uniquement : ignorer `src-tauri` côté watcher :
   ```js title="vite.config.ts"
   export default defineConfig({ server: { watch: { ignored: ["**/src-tauri/**"] } } });
   ```
6. Vérifier : `pnpm tauri dev` (variantes documentées).

## Next Steps (même fichier)

- [Project Structure](/start/project-structure/) → `references/project-structure.md`
- [Frontend Framework](/start/frontend/) → `references/frontend-*.md`
- [CLI Reference](/reference/cli/) → skill `tauri-config-cli-reference`
- [Develop](/develop/) → skill `tauri-ipc-bridge`
- [Plugins](/plugin/) → skill `tauri-plugins-catalogue`
