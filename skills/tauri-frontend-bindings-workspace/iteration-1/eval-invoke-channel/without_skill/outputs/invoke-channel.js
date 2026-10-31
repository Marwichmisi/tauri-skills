import { invoke, Channel } from '@tauri-apps/api';
const ch = new Channel();
await invoke('download', { url: 'https://tauri.app', onEvent: ch });
