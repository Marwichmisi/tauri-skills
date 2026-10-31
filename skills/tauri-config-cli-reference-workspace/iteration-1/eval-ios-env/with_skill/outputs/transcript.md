# Transcript — eval 2 ios-env (with skill)

## Skill steps (Workflow SKILL.md + Routage)

1. Intention : CLI dev iOS + nommer des variables d'environnement (hooks inclus)
   → Routage : `references/cli.md` + `references/environment.md`.
2. Lu : `SKILL.md` (Workflow/Routage/Frontières, commit `ec113a50`).
3. Lu : `references/environment.md` (règle priorité flag, entrées CLI,
   complément `_cli_ios.mdx` TAURI_DEV_HOST, hooks TAURI_ENV_* lecture seule).
4. Lu : `references/cli.md` (iOS hôte macOS seul, init/dev/build, --port /
   TAURI_CLI_PORT, homonyme `tauri cli` rejeté).
5. Appliqué : `examples/cli-commands.sh` (pnpm tauri ios init/dev/build),
   `examples/env.sh` (CI, TAURI_CLI_PORT, règle flag prime).
6. Écrit `outputs/ios-commands.sh` + `outputs/env.conf` (dirs créés).
7. Validé avec `scripts/check-config-cli.py --cli` / `--env` avant sauvegarde.

## Script OK lines

```
OK .../outputs/ios-commands.sh: dev=['ios'], in-app=—
OK .../outputs/env.conf: variables=['CI', 'TAURI_CLI_PORT', 'TAURI_DEV_HOST']
```

Full paths :
- OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-config-cli-reference-workspace/iteration-1/eval-ios-env/with_skill/outputs/ios-commands.sh: dev=['ios'], in-app=—
- OK /media/marwane/70C22D9422EFD8893/tauri/skills/skills/tauri-config-cli-reference-workspace/iteration-1/eval-ios-env/with_skill/outputs/env.conf: variables=['CI', 'TAURI_CLI_PORT', 'TAURI_DEV_HOST']
