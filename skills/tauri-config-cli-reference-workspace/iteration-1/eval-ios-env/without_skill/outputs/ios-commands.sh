#!/bin/bash
set -euo pipefail

# Build iOS sur macOS — Tauri CLI via pnpm
# Prérequis: macOS + Xcode + rustup target add aarch64-apple-ios

export TAURI_CLI_PORT=1430
# Décommenter en CI :
# export CI=true
# Pour device physique, décommenter :
# export TAURI_DEV_HOST=$(ipconfig getifaddr en0)

pnpm install
pnpm tauri ios init

# Dev simulateur :
# pnpm tauri ios dev

# Dev device physique :
# pnpm tauri ios dev -- --device

# Build release :
# CI=true pnpm tauri ios build
