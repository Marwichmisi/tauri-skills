# Gabarit de skill — reproductible pour les 12 domaines

> Décisions verrouillées : tickets #3 (découpage), #4 (gabarit+prototype),
> #5 (contrat skill-creator). Vocabulaire imposé : voir `GLOSSARY.md`
> (**domaine**, **routage**, **catalogue**).

## Arborescence imposée

```
skills/<nom>/
├── SKILL.md            # manifesto < 500 lignes : workflow + tableau de routage + frontières
├── references/         # extraits fidèles de tauri-docs, un fichier par sous-domaine
├── examples/           # snippets minimaux issus de la doc
├── scripts/            # UNIQUEMENT si besoin réel (check déterministe ciblé)
├── tests/              # tests du/des scripts (seams basses)
└── evals/evals.json    # 2-3 prompts + expectations (skill-creator, pas figés par la spec)
```

## SKILL.md — manifesto (< 500 lignes)

Frontmatter : `name: tauri-*`, `description` pushy déclarant frontières
et renvois inter-skills (ex : « Use me whenever … — I own the doctrine,
plugin fiches only refer to me »).

Corps :
1. `> Source-de-vérité` : `tauri-docs/` commit `ec113a50`, EN canonique seule.
2. `## Workflow` : identifier intention → router → appliquer exemple → lancer script → renvoyer frères.
3. `## Routage` : tableau `Intention | Lire en premier | Exemple | Script` (snippet décisionnel du prototype).
4. `## Frontières` : ce que le skill ne fait pas + renvois nommés vers frères.
5. `## Règle anti-drift` : pointeur `Source:` par extrait, aucune permission inventée, détail en `references/`.
6. `## Exemple minimal` : pointeurs vers `examples/` + commande de validation.

## references/ — fidélité

- Un `.md` par sous-**domaine**, copie fidèle avec en-tête `Source: <doc-path>, commit ec113a50, titre frontmatter`.
- Jamais de contenu inventé. API Rust linkée (`docs.rs`), jamais copiée. Références générées (config/ACL/JS) régénérées avant écriture.
- Cas sécurité : `capabilities.md`, `permissions.md`, `scopes.md`, `hardening.md` (CSP/asset-protocol/headers/lifecycle), `plugin-permissions.md` (using/writing + windows-platforms).

## examples/ — minimalité

Snippets tirés de la doc, pas réécrits : `default-capability.json` (`security/capabilities.mdx`), `tauri.conf.json` (activation `security.capabilities`), `permission-toml-example.toml` (`security/permissions.mdx`).

## scripts/ — ciblé, pas systématique

Un seul script par besoin discriminant, repris de l'étalon prototype :
`check-capabilities.py` (valide identifier, cibles windows/webviews, forme `plugin:…` ou set kébab, cas OK/KO testés).
Format permission accepté : `plugin:perm` (`fs:default`), `plugin:scope:cle` (`core:window:allow-set-title`), ou set nu kébab (`allow-home-read-extended`) — `foo` nu rejeté.

## evals/ — skill-creator

`evals/evals.json` : 2-3 prompts réalistes + `expected_output` + `expectations` vérifiables (schéma `references/schemas.md` de skill-creator).
Boucle : runs with-skill vs baseline en parallèle → grading (`.agents/skills/skill-creator/agents/grader.md`) → `benchmark.json` → viewer statique → itération.
Ce ticket #7 livre l'itération 1 du pilote (`skills/tauri-security-capabilities-workspace/iteration-1/`).

## Réutilisation pour les 11 suivants

Copier `skills/tauri-security-capabilities/` comme étalon, remplacer `references/`/`examples/` par le périmètre du **domaine** (voir `docs/TRACABILITE.md`), garder workflow/**routage**/frontières/anti-drift à l'identique. Le **catalogue** (`tauri-plugins-catalogue`) reste un routeur unique vers 30 `references/*.md`, sans dupliquer la doctrine sécurité.
