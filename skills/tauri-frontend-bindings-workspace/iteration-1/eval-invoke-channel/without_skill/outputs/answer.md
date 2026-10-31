# Baseline sans skill — invoke-channel (mémoire modèle)

Je vais appeler la commande download avec un Channel.

```js
import { invoke, Channel } from '@tauri-apps/api';
const ch = new Channel();
await invoke('download', { url: 'https://tauri.app', onEvent: ch });
```

Côté Rust :

```rust
#[tauri::command]
async fn download(url: String, ch: Channel<String>) -> Result<()> {
  ch.send("done".to_string())?;
  Ok(())
}
```

Ça devrait marcher avec Tauri v2.
