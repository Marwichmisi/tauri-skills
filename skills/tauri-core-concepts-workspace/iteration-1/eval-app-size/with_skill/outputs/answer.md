# Réduire la taille du binaire Tauri

Source : `tauri-docs/src/content/docs/concept/size.mdx`, commit `ec113a50`, titre `App Size` (via `references/app-size.md` du skill `tauri-core-concepts`).

## 1. Profil Cargo stable (recommandé)

La doc recommande de rester sur la toolchain stable sauf utilisateur avancé. Ajouter dans `src-tauri/Cargo.toml` :

```toml
# src-tauri/Cargo.toml
[profile.dev]
incremental = true # Compile your binary in smaller steps.

[profile.release]
codegen-units = 1 # Allows LLVM to perform better optimization.
lto = true # Enables link-time-optimizations.
opt-level = "s" # Prioritizes small binary size. Use `3` if you prefer speed.
panic = "abort" # Higher performance by disabling panic handlers.
strip = true # Ensures debug symbols are removed.
```

Notes :
- `opt-level = "s"` priorise la petite taille ; mettre `3` si on préfère la vitesse. Option `z` = taille max (documentée, non retenue ici).
- Ne pas utiliser les options nightly (`rustflags = ["-Zthreads=8"]`, `trim-paths = "all"`, `-Cdebuginfo=0`) sur stable.
- `panic = "abort"` désactive les handlers de panic (gain perf/taille, mais pas de unwind).

## 2. Retirer les commandes inutilisées

Dans `tauri.conf.json` :

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

Effet : retire les commandes jamais autorisées dans les fichiers de capability (ACL), pour ne pas payer ce qu'on n'utilise pas.

Pour maximiser le gain : ne déclarer en ACL que les commandes réellement utilisées, au lieu d'utiliser les `defaults`.

## 3. Prérequis de version

`removeUnusedCommands` exige :
- `tauri@2.4`
- `tauri-build@2.1`
- `tauri-plugin@2.1`
- `tauri-cli@2.4`

## 4. Mise en garde

> This won't be accounting for dynamically added ACLs at runtime so make sure to check it when using this.

Si des ACL sont ajoutées dynamiquement au runtime, elles ne seront pas prises en compte : les commandes correspondantes risquent d'avoir été retirées à la compilation. Vérifier ce cas avant d'activer l'option.
