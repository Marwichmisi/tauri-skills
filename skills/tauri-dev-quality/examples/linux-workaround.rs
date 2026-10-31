// Tiré de develop/Debug/linux-graphics.md (workaround WebKitGTK/NVIDIA).
// Ordre doc : 1) nvidia_drm.modeset=1 (noyau) 2) __NV_DISABLE_EXPLICIT_SYNC=1
// 3) WEBKIT_DISABLE_DMABUF_RENDERER=1 4) WEBKIT_DISABLE_COMPOSITING_MODE=1.
// Ne shipper un override inconditionnel que si l'app est vérifiée affectée
// (désactive un fast path pour tous, y compris setups sains).
fn main() {
  // Workaround for WebKitGTK on NVIDIA, see tauri-apps/tauri#9394
  #[cfg(target_os = "linux")]
  std::env::set_var("WEBKIT_DISABLE_DMABUF_RENDERER", "1");

  tauri::Builder::default()
    // ...
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
