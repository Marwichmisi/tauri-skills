import { Command } from '@tauri-apps/plugin-shell';
await Command.create('open', ['https://tauri.app']).execute();
