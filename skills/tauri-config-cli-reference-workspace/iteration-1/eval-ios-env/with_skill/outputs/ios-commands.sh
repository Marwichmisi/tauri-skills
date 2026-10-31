# iOS sur hôte macOS seul (reference/_cli_ios.mdx) — pnpm variants (reference/_cli.mdx CommandTabs).
# Ne jamais lancer `tauri cli` : commande dev inexistante (homonyme, voir references/cli.md).
# Règle env : si variable + flag coexistent, le flag prime (references/environment.md).

# Init cible iOS (gen/ios) :
pnpm tauri ios init

# Dev iOS (hot-reload Rust, utilise build.devUrl + build.beforeDevCommand) :
# CI=true (mode sans interaction) + TAURI_CLI_PORT=1430 via env (voir env.conf) ;
# --port prime sur TAURI_CLI_PORT en cas de conflit :
CI=true pnpm tauri ios dev --port 1430

# Build release + IPA :
pnpm tauri ios build
