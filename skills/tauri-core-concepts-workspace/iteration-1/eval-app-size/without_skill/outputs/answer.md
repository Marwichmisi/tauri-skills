# Réduire la taille du binaire Tauri

## 1. Profil Cargo `release` qui minimise la taille (stable uniquement)

Dans `src-tauri/Cargo.toml` :

```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
strip = true
```

Effets :
- `opt-level = "z"` : optimise pour la taille (plus agressif que `"s"`).
- `lto = true` : Link-Time Optimization, fusionne et élimine le code mort entre crates.
- `codegen-units = 1` : une seule unité de codegen → meilleure optimisation LTO, binaire plus petit.
- `strip = true` : supprime les symboles de debug.

Prérequis version :
- Toolchain **Rust stable** suffit, pas besoin de nightly.
- `strip = true` dans le profil nécessite **Rust >= 1.59** (stabilisé à 1.59). Avec un Rust stable récent, OK.
- Ne pas utiliser `build-std`, `cranelift`, `opt-level = "xs"` ou `-Z` : ce sont du nightly / instable.

## 2. Option `tauri.conf.json` qui retire les commandes inutilisées

Dans `src-tauri/tauri.conf.json` :

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

Prérequis version :
- Nécessite **Tauri v1.0+** (crate `tauri` v1 et `@tauri-apps/cli` v1 à jour, recommandé >= 1.2).
- Ne fonctionne qu'au build via `tauri build` / `tauri dev` (c'est le CLI qui fait l'analyse).

## 3. Mise en garde

- `lto = true` + `codegen-units = 1` : **temps de compilation release beaucoup plus long**. Ne l'active que pour le build final.
- `strip = true` : **perte des symboles** → stacktraces / debug en production inexploitables. Garde une copie non-strippée si tu dois diagnostiquer un crash.
- `removeUnusedCommands: true` : analyse statique du code Rust + JS. Si tu invoques une commande de façon dynamique (nom construit en string, `invoke(cmdVar)`, macro), elle peut être **supprimée à tort** alors qu'elle est utilisée → `invoke` échoue au runtime. **Teste le binaire release de bout en bout** après activation.
- Ne pas combiner avec `panic = "abort"` sans vérifier : certaines dépendances exigent `unwind`, et ça casse `catch_unwind` / backtraces. Le profil ci-dessus l'évite volontairement pour rester sûr sur stable.

## Fichiers fournis

- `Cargo.toml` : extrait avec le `[profile.release]` minimal stable.
- `tauri.conf.json` : extrait minimal avec `build.removeUnusedCommands`.
