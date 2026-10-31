use std::sync::atomic::{AtomicBool, Ordering};
use tauri::{AppHandle, Manager};

// Shared setup state: tracks whether frontend signalled it is ready.
pub struct SetupState {
    complete: AtomicBool,
}

impl SetupState {
    pub fn new() -> Self {
        Self {
            complete: AtomicBool::new(false),
        }
    }

    // Called from frontend via command `set_complete` once main window is ready.
    pub fn set_complete(&self) {
        self.complete.store(true, Ordering::SeqCst);
    }

    pub fn is_complete(&self) -> bool {
        self.complete.load(Ordering::SeqCst)
    }
}

#[tauri::command]
pub fn set_complete(state: tauri::State<SetupState>, app: AppHandle) {
    // Mark setup as complete, then swap windows.
    state.set_complete();

    // Close splashscreen and show main window.
    if let Some(splash) = app.get_webview_window("splashscreen") {
        let _ = splash.close();
    }
    if let Some(main) = app.get_webview_window("main") {
        let _ = main.show();
        let _ = main.set_focus();
    }
}

// Fallback: auto-close splashscreen after timeout using tokio::time.
pub fn spawn_splash_fallback(app: AppHandle) {
    tauri::async_runtime::spawn(async move {
        // Give frontend up to 5s to call set_complete, then force show.
        tokio::time::sleep(std::time::Duration::from_secs(5)).await;

        let state = app.state::<SetupState>();
        if state.is_complete() {
            return;
        }
        // Timeout reached without set_complete: close splash, show main anyway.
        if let Some(splash) = app.get_webview_window("splashscreen") {
            let _ = splash.close();
        }
        if let Some(main) = app.get_webview_window("main") {
            let _ = main.show();
        }
    });
}

pub fn init_setup(app: &mut tauri::App) -> Result<(), Box<dyn std::error::Error>> {
    app.manage(SetupState::new());
    let handle = app.handle().clone();
    spawn_splash_fallback(handle);
    Ok(())
}
