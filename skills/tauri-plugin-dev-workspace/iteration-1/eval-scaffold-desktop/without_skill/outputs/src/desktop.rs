use serde::de::DeserializeOwned;
use tauri::{plugin::PluginApi, AppHandle, Runtime};

/// Desktop implementation of `my-plugin`.
pub struct MyPlugin<R: Runtime> {
    _app: AppHandle<R>,
}

impl<R: Runtime> MyPlugin<R> {
    pub fn new(app: AppHandle<R>, _api: PluginApi<R, Option<serde_json::Value>>) -> Self {
        Self { _app: app }
    }
}

/// Helper used by `lib.rs` setup on desktop targets.
pub fn init<R: Runtime>(app: &AppHandle<R>, _config: Option<serde_json::Value>) -> crate::Result<()> {
    let _ = app;
    Ok(())
}

fn _assert_deserialize<T: DeserializeOwned>() {}
