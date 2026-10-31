use serde::{Deserialize, Serialize};
use std::path::PathBuf;
use tauri::Runtime;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct CameraRequest {
    pub quality: usize,
    pub allow_edit: bool,
}

#[derive(Deserialize)]
pub struct Photo {
    pub path: PathBuf,
}

impl<R: Runtime> crate::MyPlugin<R> {
    pub fn open_camera(&self, payload: CameraRequest) -> crate::Result<Photo> {
        self.0
            .run_mobile_plugin("openCamera", payload)
            .map_err(Into::into)
    }
}
