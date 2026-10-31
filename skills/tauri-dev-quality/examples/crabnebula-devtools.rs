// Tiré de develop/Debug/crabnebula-devtools.mdx.
// Instrumente l'app (assets, tauri.conf, logs, spans, commands, events)
// et l'expose au DevTools CrabNebula en debug uniquement (recommandé).
fn main() {
    // This should be called as early in the execution of the app as possible
    #[cfg(debug_assertions)] // only enable instrumentation in development builds
    let devtools = tauri_plugin_devtools::init();

    let mut builder = tauri::Builder::default();

    #[cfg(debug_assertions)]
    {
        builder = builder.plugin(devtools);
    }

    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
