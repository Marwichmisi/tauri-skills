# Transcript — eval scaffold desktop `my-plugin` (avec skill)

## Étapes
1. Lu `skills/tauri-plugin-dev/SKILL.md` → routage intention "Nommer/scaffolder" → `references/plugin-basics.md` + exemples `Cargo.plugin.toml`, `lib-plugin.rs`, `commands-upload.rs`, `guest-js-upload.js`, `tauri-conf-plugin.json` + script `--identifier/--invoke` (+ `--cargo` pour support plateformes).
2. Lu `references/plugin-basics.md` (Sources commit `ec113a50`, titre `Plugin Development`, fichier `tauri-docs/src/content/docs/develop/Plugins/index.mdx`) + les 5 exemples + `scripts/check-plugin-dev.py` (modes `--identifier/--permission/--cargo/--invoke`).
3. Lu `tests/test_check_plugin_dev.py` + `evals/evals.json` (eval id 1 : attentes `Builder::new("my-plugin")` + `invoke_handler` upload, `invoke('plugin:my-plugin|upload')` + `Channel`, checks OK, citation `develop/Plugins/index.mdx` commit `ec113a50`).
4. Créé `outputs/` (`mkdir -p`) ; écrit 6 artefacts (copies fidèles des exemples, aucun identifiant inventé) : `commands.rs`, `lib.rs`, `desktop.rs`, `mobile.rs`, `guest-js-upload.js`, `Cargo.plugin.toml`, `tauri-conf-plugin.json`.
5. Lancé les 4 checks (voir sorties ci-dessous) : tous `rc=0`.
6. Écrit `answer.md` (réponse complète + pointeurs source fichier+commit+titre) + ce `transcript.md`.

## Checks — commandes et sorties exactes
### `--identifier`
```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --identifier my-plugin
OK identifier 'my-plugin' valide (develop/Plugins/index.mdx)
rc=0
```
### `--cargo`
```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --cargo skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/Cargo.plugin.toml
OK skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/Cargo.plugin.toml: platforms.support fidèle (windows=full, linux=full, macos=full, android=partial, ios=none)
rc=0
```
### `--invoke` guest-js
```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --invoke skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/guest-js-upload.js
OK skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/guest-js-upload.js: invoke plugin fidèle
 - invoke plugin:my-plugin|upload
rc=0
```
### `--invoke` lib.rs
```
$ python3 skills/tauri-plugin-dev/scripts/check-plugin-dev.py --invoke skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/lib.rs
OK skills/tauri-plugin-dev-workspace/iteration-1/eval-scaffold-desktop/with_skill/outputs/lib.rs: invoke plugin fidèle
 - Builder::new("my-plugin")
rc=0
```

## Notes
- `commands.rs` seul volontairement non soumis à `--invoke` : le check exige `Builder::new`/`invoke_handler` (erreur `commande Rust sans Builder::new ni invoke_handler` sinon) ; l'enregistrement vit dans `lib.rs` conformément à la doc.
- `desktop.rs`/`mobile.rs` : stubs `MyPlugin` pascal-case (phrase doc § Exposer Rust) + commentaires source ; pas de `#[command]` isolé pour ne pas déclencher le garde-fou `--invoke`.
- Aucune URL inventée ; API Rust linkée (`docs.rs`), jamais copiée ; traductions ignorées, EN canonique seule.
