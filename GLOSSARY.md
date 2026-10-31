# Pack de skills Tauri v2

Spécification du découpage d'un pack de skills adossé à `tauri-docs/` v2 comme source de vérité, pour agents suivant les best practices Tauri.

## Language

**Domaine**:
Un chunk de la doc Tauri qui mérite son skill (ex: sécurité, distribution).
_Avoid_: module, section

**Routage**:
La règle dans `SKILL.md` qui envoie vers le bon `references/*.md` par sous-domaine.
_Avoid_: routing générique, dispatch

**Catalogue**:
Les 30 fiches `plugin/*` exposées via un skill routeur unique vers 30 références.
_Avoid_: liste de plugins, index
