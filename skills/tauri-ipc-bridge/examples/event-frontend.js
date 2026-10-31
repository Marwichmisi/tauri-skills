import { listen } from '@tauri-apps/api/event';

listen('download-started', (event) => {
  console.log(`downloading ${event.payload}`);
});

listen('download-progress', (event) => {
  console.log(`progress ${event.payload}`);
});
