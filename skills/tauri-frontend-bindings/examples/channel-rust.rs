// Pendant JS : new Channel<string>() + invoke('download', { onEvent })
// voir examples/invoke-channel.js
// Rust counterpart : tauri::ipc::Channel (docs.rs linkée, jamais copiée)
// https://docs.rs/tauri/2/tauri/ipc/struct.Channel.html

use tauri::ipc::Channel;

#[tauri::command]
async fn download(url: String, on_event: Channel<String>) -> tauri::Result<()> {
    on_event.send("started".to_string())?;
    on_event.send("finished".to_string())?;
    let _ = url;
    Ok(())
}
