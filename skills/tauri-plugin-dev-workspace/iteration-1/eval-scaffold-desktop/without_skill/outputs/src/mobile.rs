use serde::de::DeserializeOwned;
use tauri::{
    ipc::{Channel, InvokeBody},
    plugin::{PluginApi, PluginHandle},
    AppHandle, Runtime,
};

use crate::commands::UploadProgress;

/// Mobile bindings for `my-plugin` (Android partial, iOS none — see Cargo platforms.support).
pub trait MobileExt<R: Runtime> {
    fn my_plugin(&self) -> &MyPlugin<R>;
}

pub struct MyPlugin<R: Runtime> {
    handle: PluginHandle<R>,
}

impl<R: Runtime> MobileExt<R> for AppHandle<R> {
    fn my_plugin(&self) -> &MyPlugin<R> {
        // In a real plugin this resolves the mobile handle registered in setup.
        unimplemented!("mobile handle lookup — Android partial, iOS unsupported")
    }
}

/// Called from `lib.rs` setup on mobile targets.
pub fn init<R: Runtime>(
    _app: &AppHandle<R>,
    _api: PluginApi<R, Option<serde_json::Value>>,
) -> crate::Result<MyPlugin<R>> {
    Err(crate::Error::MobileNotSupported)
}

/// Forward `upload` to the native layer via the mobile bridge.
/// Mirrors `plugin:my-plugin|upload` with a progress Channel.
pub async fn upload_mobile<R: Runtime>(
    handle: &PluginHandle<R>,
    path: String,
    on_progress: Channel<UploadProgress>,
) -> crate::Result<String> {
    handle
        .run_mobile_plugin::<String>("upload", InvokeBody::Json(serde_json::json!({ "path": path })))
        .map_err(|e| crate::Error::Plugin(e.to_string()))?;
    let _ = on_progress;
    Ok(String::new())
}

fn _assert_deserialize<T: DeserializeOwned>() {}
