import { addPluginListener, PluginListener } from '@tauri-apps/api/core';

export async function onCamera(
  handler: (photo: { path: string }) => void
): Promise<PluginListener> {
  return await addPluginListener(
    'my-plugin',
    'camera',
    handler
  );
}
