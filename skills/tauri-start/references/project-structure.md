# Structure projet — extrait doc

Source : `tauri-docs/src/content/docs/start/project-structure.mdx`, commit `ec113a50`, titre `Project Structure`.

> A Tauri project is usually made of 2 parts, a Rust project and a JavaScript project (optional), and typically the setup looks something like this:

Voir `examples/project-structure.txt` (copie exacte de l'arbre doc) :

```
.
├── package.json
├── index.html
├── src/
│   ├── main.js
├── src-tauri/
│   ├── Cargo.toml
│   ├── Cargo.lock
│   ├── build.rs
│   ├── tauri.conf.json
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs
│   ├── icons/
│   │   ├── icon.png
│   │   ├── icon.icns
│   │   └── icon.ico
│   └── capabilities/
│       └── default.json
```

Rôles (même fichier) :

- `tauri.conf.json` : fichier principal de config, du bundle id à la dev server url. Marqueur CLI pour trouver le projet Rust. Détail schéma : skill `tauri-config-cli-reference` (`develop/configuration-files/#tauri-config`).
- `capabilities/` : dossier lu par défaut pour les [capability files](/security/capabilities/). Doctrine : skill `tauri-security-capabilities` (`security/`).
- `icons/` : sortie par défaut de [`tauri icon`](/reference/cli/#icon), référencé via `tauri.conf.json > bundle > icon`.
- `build.rs` : contient `tauri_build::build()` (système de build Tauri).
- `src/lib.rs` : code Rust + point d'entrée mobile (`#[cfg_attr(mobile, tauri::mobile_entry_point)]`). Ne pas écrire direct en `main.rs` car mobile compile en lib.
- `src/main.rs` : entrée desktop, appelle `app_lib::run()` (`app_lib` = `[lib.name]` du Cargo.toml). Ne pas modifier, éditer `lib.rs`.

> Tauri works similar to a static web host, and the way it builds is that you would compile your JavaScript project to static files first, and then compile the Rust project that will bundle those static files in.

Rust seul : supprimer le reste et utiliser `src-tauri/` comme racine ou membre du workspace.

Check : `python3 scripts/check-start.py src-tauri/tauri.conf.json --project-root .` vérifie les 5 fichiers requis (`Cargo.toml`, `build.rs`, `main.rs`, `lib.rs`, `tauri.conf.json`).
