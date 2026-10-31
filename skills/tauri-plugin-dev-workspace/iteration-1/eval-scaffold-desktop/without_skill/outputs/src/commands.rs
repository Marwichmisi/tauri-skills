use tauri::{ipc::Channel, AppHandle, Runtime};

#[derive(Debug, Clone, serde::Serialize)]
#[serde(rename_all = "camelCase")]
pub struct UploadProgress {
    pub chunk: u64,
    pub total: u64,
}

/// Upload a file with progress events forwarded over a Channel.
/// Exposed to JS as `plugin:my-plugin|upload`.
#[tauri::command]
pub async fn upload<R: Runtime>(
    _app: AppHandle<R>,
    path: String,
    on_progress: Channel<UploadProgress>,
) -> Result<String, String> {
    if path.trim().is_empty() {
        return Err("path must not be empty".into());
    }
    // Desktop implementation: stream chunks, emit progress.
    // Simplified skeleton: emit 2 events then return.
    let total = 100u64;
    for chunk in [50u64, 100u64] {
        let _ = on_progress.send(UploadProgress { chunk, total });
    }
    log::info!("my-plugin upload {}", path);
    Ok(format!("uploaded:{path}"))
}
