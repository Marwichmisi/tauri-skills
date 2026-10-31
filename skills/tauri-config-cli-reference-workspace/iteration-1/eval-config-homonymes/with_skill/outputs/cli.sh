# CLI dev (reference/_cli.mdx + reference/_cli_ios.mdx) vs usage in-app (plugin/cli.mdx).
# Dev : installer et lancer via le package manager ; in-app : lire les matches.
# Ne jamais lancer `tauri cli` : commande dev inexistante (homonyme).

# Dev CLI — installer la CLI dev et le plugin (plugin/cli.mdx Setup) :
npm run tauri add cli
pnpm tauri add cli
cargo tauri add cli

# Dev CLI — cycle dev/build (reference/_cli.mdx : tauri dev/build) :
npm run tauri dev
pnpm tauri build

# Dev CLI — iOS sur hôte macOS seul (reference/_cli_ios.mdx) :
pnpm tauri ios init
pnpm tauri ios dev
pnpm tauri ios build

# In-app CLI — lecture des matches (plugin/cli.mdx Usage, JS + Rust) :
# JS : import { getMatches } from '@tauri-apps/plugin-cli'
# Rust : app.cli().matches() via tauri_plugin_cli::init() + CliExt
# Config lue : tauri.conf.json > plugins.cli (voir tauri.conf.json ci-joint)
# Permission requise : "cli:default" en capabilities (doctrine : tauri-security-capabilities)
