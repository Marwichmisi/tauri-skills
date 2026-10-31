# Debugging — extrait doc

Sources (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Debug/index.mdx` (titre `Debug`)

## Dev-only code (même fichier)

> One of the most useful tools in your toolkit for debugging is the ability to add debugging statements in your code. However, you generally don't want these to end up in production, which is where the ability to check whether you're running in development mode or not comes in handy.

Rust (même fichier) :

```rs
fn main() {
  #[cfg(dev)]
  {
    // `tauri dev` only code
  }
  if cfg!(dev) {
    // `tauri dev` only code
  } else {
    // `tauri build` only code
  }
  let is_dev: bool = tauri::is_dev();

  #[cfg(debug_assertions)]
  {
    // Debug only code
  }
}
```

## Consoles (même fichier)

- Rust console : terminal du `tauri dev`, `println!` pour logger, `RUST_BACKTRACE=1 tauri dev` (Linux/macOS) ou `$env:RUST_BACKTRACE=1` + `tauri dev` (PowerShell Windows) pour la stack trace.
- WebView console : clic droit `Inspect Element`, ou `Ctrl+Shift+i` (Linux/Windows), `Command+Option+i` (macOS). Inspecteur = webkit2gtk WebInspector (Linux), Safari (macOS), Edge DevTools (Windows).

## Devtools programmatic (même fichier)

```rust
tauri::Builder::default()
  .setup(|app| {
    #[cfg(debug_assertions)] // only include this code on debug builds
    {
      let window = app.get_webview_window("main").unwrap();
      window.open_devtools();
      window.close_devtools();
    }
    Ok(())
  });
```

Voir `WebviewWindow::open_devtools` / `close_devtools` (lien `docs.rs` uniquement, jamais copié).

## Devtools en prod (même fichier)

- `tauri build --debug` garde la console dev dans `src-tauri/target/debug/bundle`.
- Devtools en **production** : activer la Cargo feature `devtools` dans `src-tauri/Cargo.toml` (`tauri = { version = "...", features = ["...", "devtools"] }`). Danger doc : API privée sur macOS, bloque l'acceptation App Store.
- Débugger le Core process (GDB/LLDB) : voir `references/ide-debug.md`.
