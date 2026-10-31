# Transcript — eval updater-signed (baseline, without skill)

1. Configuré `bundle.createUpdaterArtifacts=true` pour générer les artefacts `.sig` / `latest.json`.
2. Configuré `plugins.updater.endpoints` en `https` avec `{{target}}/{{arch}}/{{current_version}}` — seules variables officielles, aucune inventée.
3. Mis `plugins.updater.pubkey` avec contenu clé minisign en ligne (pas un chemin).
4. Ajouté `bundle.windows.nsis.installMode="passive"` pour Windows.
5. Vérifié JSON valide et écrit `tauri.conf.json` + `answer.md`.
