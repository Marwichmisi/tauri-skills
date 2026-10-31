import { open } from '@tauri-apps/plugin-dialog';
import { readTextFile } from '@tauri-apps/plugin-fs';

const file = await open({
  multiple: false,
  directory: false,
  filters: [{ name: 'Text', extensions: ['txt', 'md'] }]
});

if (typeof file === 'string') {
  const contents = await readTextFile(file);
  console.log(contents);
}
