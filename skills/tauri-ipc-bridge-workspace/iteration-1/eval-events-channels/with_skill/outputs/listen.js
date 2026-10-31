import { listen, once } from '@tauri-apps/api/event';

const unlistenStarted = await listen('download-started', (event) => {
  console.log(`downloading ${event.payload}`);
});
const unlistenProgress = await listen('download-progress', (event) => {
  console.log(`progress ${event.payload}`);
});

await once('download-finished', () => {
  unlistenStarted.then((fn) => fn());
  unlistenProgress.then((fn) => fn());
});
