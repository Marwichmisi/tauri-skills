import { WebviewWindow } from '@tauri-apps/api/webviewWindow';
import { listen } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api/core';
import { app } from '@tauri-apps/api/app';

if (await app.supportsMultipleWindows()) {
  console.log('multi-window supported');
}

function openDetail(id) {
  const webview = new WebviewWindow(`detail-${id}`, {
    url: `detail/${id}`,
    activityName: 'DetailActivity',
  });
  webview.once('tauri://created', () => {
    console.log('window created');
  });
  webview.once('tauri://error', (e) => {
    console.error(e);
  });
}

// File associations cold start: URLs stored in Rust before UI loads
const initialUrls = await invoke('opened_urls');
if (initialUrls.length > 0) {
  console.log(initialUrls);
}

// Warm: Rust emits "opened" when RunEvent::Opened fires at runtime
await listen('opened', (event) => {
  console.log(event.payload);
});
