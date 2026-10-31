use serde::{Deserialize, Serialize};
use tauri::{AppHandle, Runtime};

fn default_mode() -> String {
    "auto".to_string()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct OpenCameraArgs {
    pub quality: String,
    pub flash: Option<bool>,
    #[serde(default = "default_mode")]
    pub mode: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CameraResult {
    pub path: String,
}

#[tauri::command]
pub async fn open_camera<R: Runtime>(
    app: AppHandle<R>,
    args: OpenCameraArgs,
) -> Result<CameraResult, String> {
    #[cfg(mobile)]
    {
        app.run_mobile_plugin("openCamera", args)
            .map_err(|e| e.to_string())
    }
    #[cfg(not(mobile))]
    {
        let _ = app;
        Err("openCamera n'est supporté que sur mobile".into())
    }
}
