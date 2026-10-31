import { listen } from '@tauri-apps/api';
const unlisten = await listen('window-destroyed', (e) => console.log(e));
await emit('frontend loaded', { ok: true });
