# Transcript — eval 1 config-homonymes (with_skill)

Skill : `skills/tauri-config-cli-reference` (commit `ec113a50`), workflow suivi pas à pas.

## Steps suivis (cf. SKILL.md Workflow/Routage)

1. **Identifier l'intention** : valider `tauri.conf.json` in-app (`plugins.cli` + `$schema`) ET distinguer CLI dev vs in-app → deux lignes du tableau de routage.
2. **Références lues** :
   - `SKILL.md` (workflow + routage + frontières + règle anti-drift).
   - `references/config.md` (forme `plugins.cli`, `$schema` gen/schemas, fusion `--config` RFC 7396).
   - `references/cli.md` (dev `_cli.mdx`/`_cli_ios.mdx` vs in-app `plugin/cli.mdx`, `tauri cli` rejeté).
   - `references/environment.md` + `references/webviews.md` (lus pour écarter : hors périmètre eval).
3. **Exemples appliqués** :
   - `examples/tauri.conf.cli.json` → copié adapté en `outputs/tauri.conf.json` (description + args verbose `-v` + subcommand `run` debug/release, `$schema` gen/schemas).
   - `examples/cli-commands.sh` → copié adapté en `outputs/cli.sh` (dev `add/dev/build/ios` vs in-app `getMatches/CliExt`, permission `cli:default` en commentaire).
4. **Scripts lancés** :
   - `python3 skills/tauri-config-cli-reference/scripts/check-config-cli.py --config .../outputs/tauri.conf.json`
     → `OK .../tauri.conf.json: JSON valide, plugins.cli conforme (args=1)`
   - `python3 skills/tauri-config-cli-reference/scripts/check-config-cli.py --cli .../outputs/cli.sh`
     → `OK .../cli.sh: dev=['add', 'build', 'dev', 'ios'], in-app=['CliExt', 'cli:default', 'getMatches', 'plugins\\.cli', 'tauri_plugin_cli']`
5. **Frontières respectées** : aucune permission déclarée (renvoi `tauri-security-capabilities`), aucun champ/commande inventé, `SKILL.md` + références citées avec pointeurs `Source:` commit `ec113a50`.
