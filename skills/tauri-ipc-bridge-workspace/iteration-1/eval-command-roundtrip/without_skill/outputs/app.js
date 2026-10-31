import { invoke } from '@tauri-apps/api/core';

invoke('Greet', { user_name: 'Tauri' });
