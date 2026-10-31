# Traçabilité pack — 135 pages → 12 domaines + hors-pack

Commit figé : `ec113a50`. Source : `tauri-docs/src/content/docs` (EN canonique, hors traductions/blog). Vérifié par `python3 scripts/check-tracabilite.py` → OK 135/135.

| Domaine | Pages | Couverture |
|---|---|---|
| hors-pack | 10 | voir docs/tracabilite.json |
| tauri-config-cli-reference | 4 | voir docs/tracabilite.json |
| tauri-core-concepts | 7 | voir docs/tracabilite.json |
| tauri-dev-quality | 13 | voir docs/tracabilite.json |
| tauri-distribution | 22 | voir docs/tracabilite.json |
| tauri-ipc-bridge | 10 | voir docs/tracabilite.json |
| tauri-migrate | 4 | voir docs/tracabilite.json |
| tauri-plugin-dev | 2 | voir docs/tracabilite.json |
| tauri-plugins-catalogue | 30 | voir docs/tracabilite.json |
| tauri-security-capabilities | 14 | voir docs/tracabilite.json |
| tauri-start | 12 | voir docs/tracabilite.json |
| tauri-ui-recettes | 7 | voir docs/tracabilite.json |

## Notes
- `hors-pack` (10) : about/**, contribute/**, racine, _fragments — tracé mais hors pack (décision #3).
- `tauri-frontend-bindings` : 0 page locale, couvre JS généré (core + 27 guest-js) + lien docs.rs.
- `tauri-distribution` inclut `plugin/updater.mdx` ; `tauri-plugins-catalogue` = plugin/** hors updater (30).
- `tauri-ipc-bridge` inclut `learn/sidecar-nodejs.mdx` regroupé avec `develop/sidecar.mdx`.

## Reproduire

```bash
python3 scripts/check-tracabilite.py
```