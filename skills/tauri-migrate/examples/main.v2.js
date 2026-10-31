import { invoke } from "@tauri-apps/api/core";
import { readText } from "@tauri-apps/plugin-clipboard-manager";
import { WebviewWindow } from "@tauri-apps/api/webviewWindow";
import { Command } from "@tauri-apps/plugin-shell";

export async function run() {
  await invoke("greet");
  await readText();
}
