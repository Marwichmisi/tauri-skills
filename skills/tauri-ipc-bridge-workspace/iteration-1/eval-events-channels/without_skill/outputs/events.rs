use tauri::{AppHandle, Emitter};

fn download(app: AppHandle, url: String) {
  app.emit("download-done", &url).unwrap();
}
