# Mise à jour des dépendances — extrait doc

Source : `tauri-docs/src/content/docs/develop/updating-dependencies.mdx`, commit `ec113a50`, titre `Updating Dependencies`.

## npm (même fichier)

> If you are using the `tauri` package:

Voir `examples/updating-deps.sh` (onglets npm/yarn/pnpm du composant `CommandTabs`) :

- `npm install @tauri-apps/cli@latest @tauri-apps/api@latest`
- `yarn up @tauri-apps/cli @tauri-apps/api`
- `pnpm update @tauri-apps/cli @tauri-apps/api --latest`

Détection de version (même fichier) : `npm outdated @tauri-apps/cli` / `yarn outdated @tauri-apps/cli` / `pnpm outdated @tauri-apps/cli`.

## Cargo (même fichier)

> You can check for outdated packages with [`cargo outdated`](https://github.com/kbknapp/cargo-outdated) or on the crates.io pages: [tauri](https://crates.io/crates/tauri/versions) / [tauri-build](https://crates.io/crates/tauri-build/versions).

> Go to `src-tauri/Cargo.toml` and change `tauri` and `tauri-build` to `tauri-build = "%version%"` (`[build-dependencies]`) et `tauri = { version = "%version%" }` (`[dependencies]`), where `%version%` is the corresponding version number from above. Then `cd src-tauri; cargo update`. Alternatively, you can run the `cargo upgrade` command provided by [cargo-edit](https://github.com/killercup/cargo-edit) which does all of this automatically.

## Sync npm ↔ Cargo (même fichier, règle dure)

> Since the JavaScript APIs rely on Rust code in the backend, adding a new feature requires upgrading both sides to ensure compatibility. Please make sure you have the same minor version of the npm package `@tauri-apps/api` and cargo crate `tauri` synced.

> And for the plugins, we might introduce this type of changes in patch releases, so we bump the npm package and cargo crate versions together, and you need to keep the exact versions synced, for example, you need the same version (e.g. `2.2.1`) of the npm package `@tauri-apps/plugin-fs` and cargo crate `tauri-plugin-fs`.

Voir `examples/package.v2.json` + `examples/Cargo.v2-mobile.toml` (versions `2.x` syncées).
Vérifié partiellement par `scripts/check-migrate.py --package-json` (majeure 2) et `--cargo-toml` (majeure 2) ; l'égalité exacte patch-à-patch se vérifie dans la réponse (expectations d'eval), pas ici.
