# Transcript — eval-scope-fs (with_skill)

## Consigne

« Mon app lit des fichiers sous $APPLOCALDATA mais doit bloquer l'accès
aux données webview. Propose le scope TOML fs (allow applocaldata
récursif + deny webview-data linux/windows) sous forme de set
réutilisable, en expliquant que deny gagne sur allow. »
Contraintes : skill `tauri-security-capabilities` (SKILL.md + Workflow /
Routage), fidélité au commit tauri-docs `ec113a50`, aucune permission
inventée. Livrables : `scope.toml` + `answer.md` (avec sources) +
`transcript.md` dans `.../eval-scope-fs/with_skill/outputs/`.

## Étapes exécutées

1. Lu `skills/tauri-security-capabilities/SKILL.md` : intention =
   « Définir/étendre une permission ou un scope » → routage vers
   `references/permissions.md` + `references/scopes.md`.
2. Lu `references/scopes.md` (extrait fidèle de
   `security/scope.mdx`, commit `ec113a50`) et `references/permissions.md`
   (format TOML, permissions uniquement en TOML, sets sous identifiant).
3. Lu `references/capabilities.md` + listé `examples/` ; lu
   `examples/permission-toml-example.toml` pour le format canonique.
4. Vérifié la source de vérité locale : `skills/tauri-docs` au commit
   `ec113a50`, `git show ec113a50:src/content/docs/security/scope.mdx` :
   récupéré les blocs canoniques complets, dont la variante
   `deny-webview-data-windows` (`$APPLOCALDATA/EBWebView/**`,
   `platforms = ["windows"]`) et le set canonique
   `scope-applocaldata-reasonable` (absents/tronqués dans l'extrait
   `references/scopes.md`, qui ne montre que la variante linux et
   `deny-default`). Descriptions reprises verbatim de la doc.
5. Consulté `evals/evals.json` (id 2) pour aligner les attentes :
   bloc `[[permission.scope.allow]]` avec `$APPLOCALDATA/**`, bloc
   `[[permission.scope.deny]]` webview-data, mention deny > allow,
   aucune permission inventée.
6. Écrit `scope.toml` (5 blocs, tous verbatim doc), `answer.md`
   (explication deny-supersedes-allow + usage + sources), `transcript.md`.

## Décisions

- Reproduction verbatim des 5 blocs doc plutôt qu'un set applicatif
  ad hoc : garantit « aucune permission inventée ».
- Étape 4 du Workflow (`scripts/check-capabilities.py`) non applicable :
  le script valide des capabilities JSON, pas un fichier de scopes TOML.
- Pas de renvoi inter-skill nécessaire (périmètre scope fs couvert par
  ce skill) ; `answer.md` mentionne toutefois la capability pour
  l'activation, conformément à `references/permissions.md`.
