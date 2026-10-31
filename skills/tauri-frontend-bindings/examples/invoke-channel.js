import { Channel, invoke } from '@tauri-apps/api/core';

const onEvent = new Channel();
onEvent.onmessage = (message) => {
  console.log(`got download event ${message}`);
};

await invoke('download', { url: 'https://tauri.app', onEvent });
