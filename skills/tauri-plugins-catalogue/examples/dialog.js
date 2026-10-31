import { ask } from '@tauri-apps/plugin-dialog';
// when using `"withGlobalTauri": true`, you may use
// const { ask } = window.__TAURI__.dialog;

// Create a Yes/No dialog
const answer = await ask('This action cannot be reverted. Are you sure?', {
  title: 'Tauri',
  kind: 'warning',
});

console.log(answer);
// Prints boolean to the console
