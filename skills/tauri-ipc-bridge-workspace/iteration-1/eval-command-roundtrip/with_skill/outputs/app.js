import { invoke } from '@tauri-apps/api/core';

const message = await invoke('greet', { name: 'Tauri' });
console.log(message);
