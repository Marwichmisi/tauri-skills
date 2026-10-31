# Transcript — scaffold-desktop / without_skill (baseline, sans skill)

## Consigne
Scaffold plugin desktop `my-plugin` : crate `tauri-plugin-my-plugin`, `src/` (`commands.rs` upload + `desktop.rs`/`mobile.rs`/`lib.rs` + `Builder::new("my-plugin")` + `invoke_handler` upload + `setup`), guest-js `invoke('plugin:my-plugin|upload')` avec `Channel`, Cargo `platforms.support` (full desktop, android partial avec notes, ios none), `tauri.conf` `plugins.my-plugin` timeout 30. Valider avec `scripts/check-plugin-dev.py` (`--identifier`/`--cargo`/`--invoke`).

Contrainte : baseline — aucune lecture de skill, aucun outil skill.

## Étapes

1. **Localisation validator** : `find ... -name check-plugin-dev.py` → `skills/tauri-plugin-dev/scripts/check-plugin-dev.py`.
2. **Lecture validator seul** (pas de SKILL.md) pour connaître les regex attendues : `BASE_RE`, `PLUGIN_INVOKE_RE=plugin:<nom>|<cmd>`, `BUILDER_RE=Builder::new("...")`, `RUN_MOBILE_RE`, `[package.metadata.platforms.support]` avec `level full/partial/none`.
3. **Création dossier** : `mkdir -p .../eval-scaffold-desktop/without_skill/outputs/src`.
4. **Écrit `Cargo.plugin.toml`** : `[package] name="tauri-plugin-my-plugin"` + `[package.metadata.platforms.support]` windows/linux/macos `full`, android `partial` + `notes`, ios `none`.
5. **Écrit `src/lib.rs`** : `Builder::new("my-plugin")` + `.invoke_handler(generate_handler![commands::upload])` + `.setup(...)` + `Error`/`Result`.
6. **Écrit `src/commands.rs`** : `#[tauri::command] async fn upload(..., on_progress: Channel<UploadProgress>)`.
7. **Écrit `src/desktop.rs`** : struct `MyPlugin<R>` + `init(app, config)`.
8. **Écrit `src/mobile.rs`** : `run_mobile_plugin("upload", ...)` + `MobileExt`, commentaire `plugin:my-plugin|upload` pour traçabilité.
9. **Écrit `guest-js-upload.js`** : `import { invoke, Channel } from '@tauri-apps/api/core'` + `new Channel()` + `invoke('plugin:my-plugin|upload', { path, onProgress })`.
10. **Écrit `tauri.conf.json`** : `plugins.my-plugin.timeout=30`.
11. **Validation** :
    - `python3 .../check-plugin-dev.py --identifier my-plugin` → `OK identifier 'my-plugin' valide`
    - `--cargo outputs/Cargo.plugin.toml` → `OK ... platforms.support fidèle (windows=full, linux=full, macos=full, android=partial, ios=none)`
    - `--invoke outputs/guest-js-upload.js` → `OK ... invoke plugin:my-plugin|upload`
    - `--invoke outputs/src/lib.rs` → `OK ... Builder::new("my-plugin")`
    - `--invoke outputs/src/mobile.rs` → `OK ... run_mobile_plugin("upload")`
    - `python3 -c json.load(tauri.conf.json)` → `timeout==30 OK`
    - `grep` : `upload`, `Builder::new`, `invoke_handler`, `setup`, `Channel` présents.
12. **Écrit `answer.md`** (réponse complète) + `transcript.md` (ce fichier).
13. **Vérification finale `ls -R outputs/`** : `Cargo.plugin.toml`, `guest-js-upload.js`, `tauri.conf.json`, `answer.md`, `transcript.md`, `src/lib.rs`, `src/commands.rs`, `src/desktop.rs`, `src/mobile.rs`.

## Résultat
Tous les checks `--identifier` / `--cargo` / `--invoke` passent (exit 0). Squelette de bout en bout conforme à la consigne.
