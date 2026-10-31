import { addPluginListener, invoke } from '@tauri-apps/api/core';

// Permissions auto-générées
await invoke('plugin:my-plugin|checkPermissions');
await invoke('plugin:my-plugin|requestPermissions', { permissions: ['camera'] });

// Commande
await invoke('plugin:my-plugin|openCamera', { quality: 'hd', mode: 'auto' });

// Event caméra
const unlisten = await addPluginListener('my-plugin', 'camera', (event) => {
  console.log('photo:', event.payload.path);
});
