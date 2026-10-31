# Invoke + Channel — réponse

Sources : `tauri@37b3be6 packages/api/src/core.ts` (invoke, Channel, convertFileSrc),
régénéré le 2026-10-31 via sparse checkout du pin `tauri-docs ec113a50`.
Routage skill : `references/core-api.md` → `examples/invoke-channel.js` + `examples/channel-rust.rs`.

## 1. Frontend JS (copie fidèle doc)

`outputs/invoke-channel.js` (doc `core.ts` § Channel) :

```js
import { Channel, invoke } from '@tauri-apps/api/core';

const onEvent = new Channel();
onEvent.onmessage = (message) => {
  console.log(`got download event ${message}`);
};

await invoke('download', { url: 'https://tauri.app', onEvent });
```

## 2. Pendant Rust (lien docs.rs, jamais copié)

`outputs/channel-rust.rs` :

```rust
// https://docs.rs/tauri/2/tauri/ipc/struct.Channel.html
use tauri::ipc::Channel;

#[tauri::command]
async fn download(url: String, on_event: Channel<String>) -> tauri::Result<()> {
    on_event.send("started".to_string())?;
    on_event.send("finished".to_string())?;
    let _ = url;
    Ok(())
}
```

## 3. Validation

```
python3 scripts/check-frontend-bindings.py --frontend outputs/invoke-channel.js --rust outputs/channel-rust.rs
OK outputs/invoke-channel.js + outputs/channel-rust.rs
 - core imports: ['core']
 - invokes: ['download']
 - docs.rs link OK
 - tauri::ipc::Channel détecté
```

Frontières : implémentation commande côté Rust → `tauri-ipc-bridge` ;
permissions/scopes → `tauri-security-capabilities` ; schéma config → `tauri-config-cli-reference`.
