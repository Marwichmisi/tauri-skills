import { addPluginListener, PluginListener } from '@tauri-apps/api/core';

export async function onRequest(
  handler: (url: string) => void
): Promise<PluginListener> {
  return await addPluginListener(
    'my-plugin',
    'camera',
    handler
  );
}
