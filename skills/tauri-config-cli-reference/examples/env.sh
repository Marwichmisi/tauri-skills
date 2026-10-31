# Variables documentées (reference/environment-variables.mdx + _cli_ios.mdx).
# Règle doc : si variable d'environnement et flag CLI coexistent, le flag prime.

# CLI dev : CI sans interaction, port du serveur dev intégré.
CI=true
TAURI_CLI_PORT=1430

# Signature/bundle (même fichier) : clé privée jamais partagée.
TAURI_SIGNING_PRIVATE_KEY=./keys/private.key
TAURI_SIGNING_PRIVATE_KEY_PASSWORD=secret

# iOS (même fichier + _cli_ios.mdx) : équipe dev, chemin projet généré.
APPLE_DEVELOPMENT_TEAM=ABCD1234
TAURI_IOS_PROJECT_PATH=./src-tauri/gen/ios

# Hooks beforeDevCommand/beforeBuildCommand (même fichier, lecture seule côté hook) :
# TAURI_ENV_DEBUG=true en `tauri dev`, TAURI_ENV_PLATFORM=windows|darwin|linux
