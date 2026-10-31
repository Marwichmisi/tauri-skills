import { invoke } from "@tauri-apps/api/tauri";
import { readText } from "@tauri-apps/api/clipboard";
import { WebviewWindow } from "@tauri-apps/api/window";
import { Command } from "@tauri-apps/api/shell";

const mobile = !!/android|ios/.exec(process.env.TAURI_ENV_PLATFORM);

export async function run() {
  await invoke("greet");
  await readText();
}
