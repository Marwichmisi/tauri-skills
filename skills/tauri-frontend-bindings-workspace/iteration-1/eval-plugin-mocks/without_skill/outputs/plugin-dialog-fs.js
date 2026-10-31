import { openDialog } from '@tauri-apps/api/dialog';
import { readFile } from '@tauri-apps/api/fs';

const file = await openDialog({ filters: ['txt'] });
await readFile(file);
