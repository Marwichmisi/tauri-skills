# Mise à jour des dépendances (develop/updating-dependencies.mdx, commit ec113a50).

# npm : API + CLI, versions mineures syncées
npm install @tauri-apps/cli@latest @tauri-apps/api@latest
npm outdated @tauri-apps/cli

# pnpm
pnpm update @tauri-apps/cli @tauri-apps/api --latest
pnpm outdated @tauri-apps/cli

# Cargo : src-tauri/Cargo.toml -> tauri = "2", tauri-build = "2", puis :
cd src-tauri
cargo update
# alternative : cargo upgrade (cargo-edit)

# Règle sync (même fichier) : @tauri-apps/api (npm) et tauri (cargo) même
# version mineure ; chaque plugin npm/cargo en versions exactes identiques
# (ex @tauri-apps/plugin-fs 2.2.1 == tauri-plugin-fs 2.2.1).
