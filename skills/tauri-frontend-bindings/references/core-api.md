# Core API — invoke, Channel, convertFileSrc, Resource

Sources régénérées avant écriture (commit figé tauri-docs `ec113a50`) :
- `tauri@37b3be6 packages/api/src/core.ts` (`@module` invoke custom commands)
- `tauri@37b3be6 packages/api/src/mocks.ts` (`@module` test helpers)
- Rust linkée : `https://docs.rs/tauri/2/tauri/ipc/struct.Channel.html`,
  `https://docs.rs/tauri/2/tauri/ipc/struct.Resource.html`
- Régénéré le 2026-10-31 via `git clone --filter=blob:none --depth 1 --sparse`
  + `checkout 37b3be6` (pin `tauri-docs` à `ec113a50`).

> Invoke your custom commands.
> This package is also accessible with `window.__TAURI__.core` when
> `app.withGlobalTauri` in `tauri.conf.json` is set to `true`.

## invoke

```typescript
async function invoke<T>(
  cmd: string,
  args: InvokeArgs = {},
  options?: InvokeOptions
): Promise<T>
```

> Sends a message to the backend.
> ```typescript
> import { invoke } from '@tauri-apps/api/core';
> await invoke('login', { user: 'tauri', password: 'poiwe3h4r5ip3yrhtew9ty' });
> ```

`InvokeArgs = Record<string, unknown> | number[] | ArrayBuffer | Uint8Array`.
`InvokeOptions.headers` lisibles côté Rust via
[`tauri::ipc::Request::headers`](https://docs.rs/tauri/2/tauri/ipc/struct.Request.html#method.headers).

## Channel

> A message channel used to stream values from Rust to the frontend.
> A `Channel` is the JavaScript counterpart of
> [`tauri::ipc::Channel`](https://docs.rs/tauri/2/tauri/ipc/struct.Channel.html).

```typescript
import { Channel, invoke } from '@tauri-apps/api/core';
const onEvent = new Channel<string>(); // TS : générique ; en JS : new Channel()
onEvent.onmessage = (message) => {
  console.log(`got download event ${message}`);
};
await invoke('download', { url: 'https://tauri.app', onEvent });
```

Fichier JS (`examples/invoke-channel.js`) : `new Channel()` sans arg
(ctor `constructor(onmessage?)`, pas `new Channel('string')`).
Pendant Rust (lien seul, jamais copié) :
`https://docs.rs/tauri/2/tauri/ipc/struct.Channel.html`.
Voir `examples/channel-rust.rs` (avec lien docs.rs exigé par le check).

## convertFileSrc

```typescript
function convertFileSrc(filePath: string, protocol = 'asset'): string
```

> Convert a device file path to a URL that can be loaded by the webview.
> ```typescript
> import { downloadDir, join } from '@tauri-apps/api/path';
> import { convertFileSrc } from '@tauri-apps/api/core';
> const filePath = await join(await downloadDir(), 'photo.png');
> const assetUrl = convertFileSrc(filePath);
> ```

Asset protocol + scope + CSP : doctrine `tauri-security-capabilities`
(`security/asset-protocol.mdx`, `security/csp.mdx`).

## Resource

> A rust-backed resource stored through `tauri::Manager::resources_table` API.
> Several API types are resources : `Menu`, `TrayIcon`, `Image`, `Webview`.

```typescript
import { Resource } from '@tauri-apps/api/core';
await using db = await DatabaseHandle.open('test.db');
```

Règle `await using` (async dispose seule) ; `Symbol.asyncDispose` + `target es2022`
si vieux bundler. Voir source `core.ts` (section Explicit Resource Management).

## addPluginListener / permissions mobiles

```typescript
async function addPluginListener<T>(
  plugin: string, event: string, cb: (payload: T) => void
): Promise<PluginListener>
async function checkPermissions<T>(plugin: string): Promise<T>
async function requestPermissions<T>(plugin: string): Promise<T>
```

Usage plugin (ex barcode-scanner) : wrapper `addPluginListener('barcode-scanner', 'scan', cb)`
+ `unregister()`. `checkPermissions`/`requestPermissions` appellent
`plugin:<nom>|check_permissions`.

## Mocks (tests, SSG)

```typescript
import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { invoke } from '@tauri-apps/api/core';
mockIPC((cmd, args) => { if (cmd === 'greet') return `Hello, ${args.name}!`; });
await invoke('greet', { name: 'tauri' });
clearMocks();
```

`mockWindows`, `mockConvertFileSrc` : fenêtres virtuelles + URL par plateforme.
`shouldMockEvents` (2.7+) : `listen`/`emit` mockés, consomme `plugin:event`.
Voir `examples/mocks.js`. Check : import `mocks` exigé si `mockIPC` détecté.
