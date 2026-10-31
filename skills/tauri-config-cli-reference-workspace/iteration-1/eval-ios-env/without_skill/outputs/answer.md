# Préparer le build iOS sur macOS (Tauri CLI)

## 1. Prérequis macOS uniquement
Le build iOS exige macOS avec Xcode + outils ligne de commande + Rust cible iOS :
```bash
xcode-select --install
rustup target add aarch64-apple-ios aarch64-apple-ios-sim x86_64-apple-ios
```
Vérifier `xcodebuild -version` et ouvrir Xcode une fois pour accepter la licence.

## 2. Commandes `pnpm tauri ios`
```bash
pnpm tauri ios init      # génère le projet Xcode dans src-tauri/gen/apple
pnpm tauri ios dev       # dev sur simulateur / device
pnpm tauri ios build     # build release (export IPA via Xcode)
```
Ré-exécuter `init` après changement de `tauri.conf.json` (bundleIdentifier, icônes) ou mise à jour Tauri.

`ios dev -- --device` ou sélection device dans Xcode pour device physique. Le simulateur suffit pour itérer.

## 3. Ports et CI
```bash
TAURI_CLI_PORT=1430 pnpm tauri ios dev
CI=true pnpm tauri ios build
```
- `TAURI_CLI_PORT=1430` : force le port du serveur interne CLI/dev-server quand le port par défaut est occupé ou pour figer l'URL dans le frontend.
- `CI=true` : mode non-interactif, désactive les prompts (utile GitHub Actions / Xcode Cloud). Échoue vite plutôt que d'attendre une entrée.

## 4. Device physique : `TAURI_DEV_HOST`
Sur simulateur, `localhost` suffit. Sur iPhone physique, le WebView doit joindre le dev-server du Mac via LAN :
```bash
export TAURI_DEV_HOST=$(ipconfig getifaddr en0)
pnpm tauri ios dev -- --device
```
- Mac et iPhone sur le même Wi-Fi.
- `tauri.conf.json > build > devUrl` doit pointer vers `http://<TAURI_DEV_HOST>:1420` (ou port Vite).
- Autoriser les connexions entrantes (pare-feu macOS).

## 5. Hook avec `TAURI_ENV_PLATFORM` / `TAURI_ENV_DEBUG`
Dans `tauri.conf.json > build > beforeDevCommand / beforeBuildCommand`, Tauri injecte :
- `TAURI_ENV_PLATFORM=ios`
- `TAURI_ENV_DEBUG=true` (dev) / `false` (build)

Exemple `scripts/tauri-hook.sh` :
```bash
#!/bin/bash
if [ "$TAURI_ENV_PLATFORM" = "ios" ]; then
  echo "Build iOS, debug=$TAURI_ENV_DEBUG"
  if [ "$TAURI_ENV_DEBUG" = "true" ]; then
    npm run dev:ios-debug
  else
    npm run build:ios-release
  fi
fi
```
```json
{
  "build": {
    "beforeDevCommand": "scripts/tauri-hook.sh",
    "beforeBuildCommand": "scripts/tauri-hook.sh",
    "devUrl": "http://localhost:1420",
    "frontendDist": "../dist"
  }
}
```

## 6. Séquence recommandée
```bash
export TAURI_CLI_PORT=1430
export TAURI_DEV_HOST=$(ipconfig getifaddr en0)
pnpm install
pnpm tauri ios init
pnpm tauri ios dev
# puis sur device :
pnpm tauri ios dev -- --device
# release :
CI=true pnpm tauri ios build
# ouvrir dans Xcode si signature / provisioning à régler :
open src-tauri/gen/apple/*.xcodeproj
```
Signer avec un Apple Developer Team dans Xcode (Signing & Capabilities) avant l'export IPA / TestFlight.
