# Hors catalogue : updater → tauri-distribution

`plugin/updater.mdx` est exclu du catalogue (30 fiches `plugin/**` hors updater, décision #3, TRACABILITE.md). Routage : toute demande auto-update (endpoints, pubkey, `createUpdaterArtifacts`, `installMode`) part vers `tauri-distribution` (`references/pipelines-updater.md`), pas vers le catalogue.

Je ne fournis aucune permission `updater:*` ici et je n'invente rien.

Doctrine permissions : toute question capability/permission/scope se décide dans `tauri-security-capabilities` (`references/plugin-permissions.md`).

## Preuve mécanique

```
$ python3 scripts/check-catalogue.py --plugin updater --capability <cap>
FAIL: fiche 'updater' hors catalogue : plugin/updater.mdx vit dans tauri-distribution (pipelines-updater) — renvoie vers tauri-distribution, pas vers le catalogue
```

Exit code 1 : rejet avec renvoi `tauri-distribution`.

## Sources

- `references/overview.md` — `Source: tauri-docs/src/content/docs/plugin/index.mdx`, commit `ec113a50` (updater exclu).
- Chaque fiche `references/*.md` rappelle l'exclusion updater.
- `docs/TRACABILITE.md` : `tauri-plugins-catalogue` = `plugin/**` hors updater (30), `plugin/updater.mdx` → `tauri-distribution`.
