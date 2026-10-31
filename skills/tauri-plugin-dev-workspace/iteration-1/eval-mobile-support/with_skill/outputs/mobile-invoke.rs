use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tauri::{Runtime, plugin::Builder};

// Mobile : src/mobile.rs — envoie un message au code natif, récupère le résultat.
// Desktop : src/desktop.rs — implémentation Rust directe.
// Logique partagée : src/lib.rs (do_something). Voir references/mobile.md.

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CameraRequest {
    pub source: String,
    pub quality: usize,
    pub allow_edit: bool,
}

#[derive(Deserialize)]
pub struct Photo {
    pub path: PathBuf,
}

#[derive(Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct PermissionResponse {
    pub camera: String,
}

impl<R: Runtime> crate::MyPlugin<R> {
    pub fn open_camera(&self, payload: CameraRequest) -> crate::Result<Photo> {
        self.0
            .run_mobile_plugin("openCamera", payload)
            .map_err(Into::into)
    }

    pub fn check_camera_permissions(&self) -> crate::Result<PermissionResponse> {
        self.0
            .run_mobile_plugin::<PermissionResponse>("checkPermissions", serde_json::Value::Null)
            .map_err(Into::into)
    }

    pub fn request_camera_permissions(&self) -> crate::Result<PermissionResponse> {
        self.0
            .run_mobile_plugin::<PermissionResponse>("requestPermissions", serde_json::Value::Null)
            .map_err(Into::into)
    }
}

pub fn init<R: Runtime>() -> Builder<R> {
    Builder::new("my-plugin")
}
