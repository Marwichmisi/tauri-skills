# Linux Graphics — extrait doc

Source (commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/Debug/linux-graphics.md` (titre `Linux Graphics Issues`)

> On Linux, Tauri renders through WebKitGTK. On some setups, most often NVIDIA GPUs, WebKitGTK and the graphics driver disagree and you get anything from a blank window to subtle rendering problems.

## Symptômes (même fichier)

- Fenêtre blanche/vide, flicker au resize, crash silencieux au resize.
- Console : `AcceleratedSurfaceDMABuf was unable to construct a complete framebuffer`.
- Console : `Gdk-Message: Error 71 (Protocol error) dispatching to Wayland display.`

Cause doc : renderer DMABUF WebKitGTK demandant des formats que le driver NVIDIA ne fournit pas (upstream WebKitGTK 261874, forums NVIDIA RTX 4070). Voir `tauri-apps/tauri#9394`.

## Workarounds, dans l'ordre (même fichier)

1. `nvidia_drm.modeset=1` en paramètre noyau (drivers NVIDIA < 545).
2. `__NV_DISABLE_EXPLICIT_SYNC=1` (fixe souvent le crash Wayland `Error 71`, sans coût perf).
3. `WEBKIT_DISABLE_DMABUF_RENDERER=1` (fixe DMABUF + `Error 71`, perd le fast path).
4. `WEBKIT_DISABLE_COMPOSITING_MODE=1` (dernier recours crash resize, coupe la compositing accélérée).

Tester en shell, ou poser en `main()` avant création webview. Voir `examples/linux-workaround.rs` (copie exacte) :

```rust
fn main() {
  // Workaround for WebKitGTK on NVIDIA, see tauri-apps/tauri#9394
  #[cfg(target_os = "linux")]
  std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");
  tauri::Builder::default()
    // ...
}
```

> Only ship an unconditional override like this if you have verified your app is affected. It disables a faster path for everyone, including users on working setups.

Check : `python3 scripts/check-dev-quality.py --linux examples/linux-workaround.rs`.

## WebGL/canvas silencieux (même fichier)

- Création contexte WebGL2 réussit même en rasterizer logiciel : rien à catcher.
- `WEBGL_debug_renderer_info` masqué (`Apple GPU` partout) pour fingerprinting : impossible de détecter le vrai backend depuis le frontend.
- Symptôme : latence élevée / bas FPS sur vues WebGL (terminaux, éditeurs, cartes) alors que le navigateur est fluide. Recette doc : fallback non-WebGL sur Linux + setting utilisateur, ne pas faire confiance au contexte.
