# Commandes de migration documentées (start/migrate/*.mdx, commit ec113a50).
# Toujours lire la page du guide AVANT de lancer : la commande n'est pas un
# substitut au guide (danger doc from-tauri-1).

# npm
npm install @tauri-apps/cli@latest
npm run tauri migrate

# pnpm
pnpm update @tauri-apps/cli@latest
pnpm tauri migrate

# cargo
cargo install tauri-cli --version "^2.0.0" --locked
cargo tauri migrate

# Doc CLI : voir tauri-config-cli-reference (reference/_cli.mdx, section migrate).
