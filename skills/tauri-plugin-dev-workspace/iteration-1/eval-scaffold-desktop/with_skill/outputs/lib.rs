use tauri::plugin::Builder;

pub fn init<R: tauri::Runtime>() -> tauri::plugin::TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![crate::commands::upload])
        .setup(|app, api| {
            // Register state, spawn background tasks here (setup lifecycle).
            // Mobile plugins are registered here in generated template.
            Ok(())
        })
        .build()
}
