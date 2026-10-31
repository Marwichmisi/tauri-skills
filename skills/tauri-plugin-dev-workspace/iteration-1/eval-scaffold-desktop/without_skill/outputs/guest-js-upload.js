import { invoke, Channel } from '@tauri-apps/api/core';

/**
 * Upload a file via `my-plugin` with progress events.
 * @param {string} path - local file path to upload
 * @param {(p: {chunk:number,total:number}) => void} onEvent - progress callback
 */
export async function upload(path, onEvent) {
  const onProgress = new Channel();
  onProgress.onmessage = (progress) => {
    onEvent?.(progress);
  };
  return invoke('plugin:my-plugin|upload', { path, onProgress });
}
