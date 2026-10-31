# App Size — extrait doc

Source : `tauri-docs/src/content/docs/concept/size.mdx`, commit `ec113a50`, titre `App Size`.

> While Tauri by default provides very small binaries it doesn't hurt to push the limits a bit, so here are some tips and tricks for reaching optimal results.

## Cargo Configuration (même fichier)

> One of the simplest frontend agnostic size improvements you can do to your project is adding a Cargo profile to it.
>
> Dependent on whether you use the stable or nightly Rust toolchain the options available to you differ a bit. It's recommended you stick to the stable toolchain unless you're an advanced user.

Stable (même fichier, voir `examples/cargo-size-profile.toml`) :

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

Nightly — différences seules (même fichier) : `profile.dev.rustflags = ["-Zthreads=8"]`, `profile.release.trim-paths = "all"`, `profile.release.rustflags = ["-Cdebuginfo=0", "-Zthreads=8"]`.

> This is not a complete reference over all available options, merely the ones that we'd like to draw extra attention to.

Options documentées (même fichier) : `incremental`, `codegen-units`, `lto`, `opt-level` (`3` vitesse, `z` taille max, `s` intermédiaire), `panic`, `strip`, `rpath`, `trim-paths`, `rustflags` (`-Cdebuginfo=0`, `-Zthreads=8`).

## Remove Unused Commands (même fichier, voir `examples/remove-unused-commands.json`)

```json title=tauri.conf.json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

> to remove commands that're never allowed in your capability files (ACL), so you don't have to pay for what you don't use

> To maximize the benefit of this, only include commands that you use in the ACL instead of using `defaults`s

> This feature requires `tauri@2.4`, `tauri-build@2.1`, `tauri-plugin@2.1` and `tauri-cli@2.4`

> This won't be accounting for dynamically added ACLs at runtime so make sure to check it when using this

Under the hood (même fichier) : `tauri-cli` ↔ `tauri-build` + build scripts `tauri`/`tauri-plugin` via env `REMOVE_UNUSED_COMMANDS` (= `src-tauri` dir) ; `generate_handler` retire les commandes inutilisées. Détail d'implémentation instable, ne pas le poser soi-même.
