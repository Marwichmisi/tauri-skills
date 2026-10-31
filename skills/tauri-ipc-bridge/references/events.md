# Events, channels, eval — extrait doc

Sources (toutes commit `ec113a50`, EN canonique) :
- `tauri-docs/src/content/docs/develop/calling-frontend.mdx` (titre `Calling the Frontend from Rust`)
- `tauri-docs/src/content/docs/develop/_sections/frontend-listen.mdx` (titre `Calling the Frontend from Rust`)
- `tauri-docs/src/content/docs/develop/calling-rust.mdx` (titre `Calling Rust from the Frontend`, section `Event System`)

## Event vs command (calling-frontend.mdx, calling-rust.mdx)

> The event system was designed for situations where small amounts of data need to be streamed or you need to implement a multi consumer multi producer pattern (e.g. push notification system).

> The event system is not designed for low latency or high throughput situations. See the channels section for the implementation optimized for streaming data.

> The major differences between a Tauri command and a Tauri event are that events have no strong type support, event payloads are always JSON strings making them not suitable for bigger messages and there is no support of the capabilities system to fine grain control event data and channels.

> The `AppHandle` and `WebviewWindow` types implement the event system traits `Listener` and `Emitter`. Events are either global (delivered to all listeners) or webview-specific (only delivered to the webview matching a given label).

> Unlike commands, events are not type safe, are always async, cannot return values and only supports JSON payloads.

## Emettre cote Rust (calling-frontend.mdx)

Global (`Emitter#emit`) et webview (`Emitter#emit_to`, `Emitter#emit_filter` + `EventTarget`) :

```rust
app.emit("download-started", &url).unwrap();
app.emit_to("login", "login-result", result).unwrap();
app.emit_filter("open-file", path, |target| match target {
  EventTarget::WebviewWindow { label } => label == "main" || label == "file-viewer",
  _ => false,
}).unwrap();
```

> Global events are delivered to **all** listeners. Webview-specific events are **not** triggered to regular global event listeners. To listen to **any** event you must use the `listen_any` function instead of `listen`.

Payload (meme fichier) : `any Clone + Serialize`, conseille `#[serde(rename_all = "camelCase")]`. Voir `examples/event-rust.rs` (download started/progress/finished).

## Ecouter cote frontend (frontend-listen.mdx)

Voir `examples/event-frontend.js` :

```ts
import { listen } from '@tauri-apps/api/event';
listen<DownloadStarted>('download-started', (event) => {
  console.log(`downloading ${event.payload.contentLength} bytes from ${event.payload.url}`);
});
```

Webview : `getCurrentWebviewWindow().listen('logged-in', ...)`. Nettoyage : `listen` rend une promesse vers `unlisten` — `const unlisten = await listen(...); unlisten()` ; `await` obligatoire (sinon `unlisten` est une promesse, pas une fonction). `once('ready', ...)` pour une seule ecoute. Emis frontend aussi recus par ces APIs (voir calling-rust.mdx).

Piges doc (meme fichier) : ne pas appeler `unlisten` avant resolution ; setup frameworks (React/Vue/Svelte) : enregistrer apres mount (`useEffect`, `onMounted`, `$effect`) + cleanup ; ordre non garanti en async rapide -> preferer Channels pour delivre ordonne.

> Events emitted in the frontend also trigger listeners registered by these APIs.

Global JS : `emit('file-selected', ...)` / `emitTo('settings', ...)` ; webview : `appWebview.emit(...)` / `emitTo('editor', ...)` ; catch-all : `listen('state-changed', ..., { target: { kind: 'Any' } })`.

## Ecouter cote Rust (frontend-listen.mdx)

Global : `app.listen("download-started", ...)` (+ `serde_json::from_str` du payload). Webview : `app.get_webview_window("main").listen("logged-in", ...)`. Stop : `app.unlisten(id)` ou `handle.unlisten(event.id)` ; `app.once("ready", ...)` (desenregistre apres premier declenchement).

## Channels (calling-frontend.mdx + calling-rust.mdx)

> Under the hood [events] directly evaluate JavaScript code so it might not be suitable to sending a large amount of data. Channels are designed to be fast and deliver ordered data. They are used internally for streaming operations such as download progress, child process output and WebSocket messages.

Rust : `reader: tauri::ipc::Channel<DownloadEvent>` + `on_event.send(...).unwrap()` (enum `Started/Progress/Finished`, `tag/event`). JS : `new Channel()` + `onmessage` + `invoke('download', { url, onEvent })`. Voir aussi `load_image(path, reader: Channel<&[u8]>)` cote calling-rust.mdx.

## Eval JS (calling-frontend.mdx)

> To directly execute any JavaScript code on the webview context you can use the `WebviewWindow#eval` function : `webview.eval("console.log('hello from Rust')")`. If the script is not so simple and must use input from Rust objects we recommend the `serialize-to-javascript` crate.

API Rust linkee, jamais copiee : `AppHandle`, `WebviewWindow`, `Listener`, `Emitter`, `emit`, `emit_to`, `emit_filter`, `Clone`, `Serialize` (liens `docs.rs` en bas du fichier doc).
