# PROTOTYPE THROWAWAY — Gabarit de skill + exemple `tauri-security-capabilities`

Question : à quoi ressemble un skill du pack (structure, routage, fidélité doc) ?
Jette après verdict. Ne merge jamais dans `main`. Voir ticket.

## Lancer

```bash
python3 prototypes/gabarit-tauri-security/scripts/check-capabilities.py prototypes/gabarit-tauri-security/examples/default-capability.json
```

Attendu : `OK` + liste des permissions. Modifie le JSON (retire `identifier`, mets une permission `foo`) pour voir les erreurs.

## Ce qui est générique (gabarit pour les 12) vs spécifique (exemple sécurité)

- Générique : arborescence `SKILL.md + references/ + examples/ + scripts/` (scripts seulement si besoin, cf. Q7), `SKILL.md <500 lignes` avec tableau de routage, `description` pushy avec frontières + renvois, règle source-de-vérité (ne citer que `tauri-docs/ ec113a50`).
- Spécifique ici : `references/capabilities.md`, `references/permissions.md` (extraits `security/`), `examples/default-capability.json`, `scripts/check-capabilities.py`.

## Fichiers

- `SKILL.md` — exemple instancié, à lire en premier.
- `references/capabilities.md`, `references/permissions.md` — extraits doc, avec pointeur source.
- `examples/default-capability.json`, `examples/tauri.conf.json` — snippets doc.
- `scripts/check-capabilities.py` — check déterministe, pas de logique métier.
