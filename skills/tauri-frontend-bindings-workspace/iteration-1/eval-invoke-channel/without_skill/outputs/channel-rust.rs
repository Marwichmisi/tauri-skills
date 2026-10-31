#[tauri::command]
async fn download(url: String, ch: Channel<String>) -> Result<()> {
  ch.send("done".to_string())?;
  Ok(())
}
