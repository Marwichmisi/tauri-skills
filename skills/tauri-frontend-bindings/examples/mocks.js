import { mockIPC, clearMocks } from '@tauri-apps/api/mocks';
import { invoke } from '@tauri-apps/api/core';

mockIPC((cmd, args) => {
  if (cmd === 'greet') {
    return `Hello, ${(args).name}!`;
  }
});

await invoke('greet', { name: 'tauri' });

clearMocks();
