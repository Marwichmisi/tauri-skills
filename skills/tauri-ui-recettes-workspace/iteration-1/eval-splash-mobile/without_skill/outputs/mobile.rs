use tauri::{Manager, RunEvent};

// mobile.rs — file associations (png/jpg) + RunEvent::Opened cold/warm handling.

pub fn handle_opened_urls(app: &tauri::AppHandle, urls: Vec<url::Url>) {
    for url in &urls {
        println!("opened file: {}", url);
        // Forward to main window frontend.
        if let Some(main) = app.get_webview_window("main") {
            let _ = main.emit("file-opened", url.to_string());
            let _ = main.show();
            let _ = main.set_focus();
        }
    }
}

pub fn run_with_file_associations(app: tauri::App) {
    app.run(|handle, event| match event {
        // Warm case: app already running, user double-clicks png/jpg.
        RunEvent::Opened { urls } => {
            println!("warm open: {} url(s)", urls.len());
            handle_opened_urls(handle, urls);
        }
        // Cold case: app launched by opening a png/jpg file.
        // On macOS/Windows Tauri delivers RunEvent::Opened at startup too,
        // but ensure main window is visible even if it was hidden for splashscreen.
        RunEvent::Ready => {
            println!("cold start ready");
            // If launched with file, Opened will follow; ensure splashscreen flow still works.
            if let Some(main) = handle.get_webview_window("main") {
                // Keep hidden until set_complete or fallback shows it.
                let _ = main.hide();
            }
        }
        RunEvent::ExitRequested { .. } => {}
        _ => {}
    });
}
