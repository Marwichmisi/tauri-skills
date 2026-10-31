import { listen } from '@tauri-apps/api/event';

const unlisten = listen('download-started', (event) => {
  console.log(event.payload);
});
unlisten();
