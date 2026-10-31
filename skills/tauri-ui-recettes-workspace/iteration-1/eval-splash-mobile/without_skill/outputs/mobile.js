import { WebviewWindow } from "@tauri-apps/api/webviewWindow";
import { invoke } from "@tauri-apps/api/core";

// mobile.js — splashscreen handshake + mobile secondary window.

// 1. Called from main window frontend once ready (e.g. after app mounted).
export async function notifySetupComplete() {
  await invoke("set_complete");
}

// 2. Splashscreen frontend: listen for progress then notify main.
// (splashscreen.html loads this too; no-op if command missing)
export async function splashscreenTick(progress) {
  const bar = document.getElementById("progress");
  if (bar) bar.style.width = `${progress}%`;
}

// 3. Mobile: open a secondary window/activity.
// On Android, activityName controls the native Activity class used.
// Requires capability "allow-create-webview-window".
export async function openMobileWindow() {
  const second = new WebviewWindow("second", {
    url: "/second",
    title: "Second",
    width: 400,
    height: 300,
    // Android-specific: custom activity for this window.
    activityName: "com.example.splashmobile.SecondActivity",
  });

  second.once("tauri://created", () => {
    console.log("second window created");
  });
  second.once("tauri://error", (e) => {
    console.error("create window failed (check capability allow-create-webview-window)", e);
  });
  return second;
}

// 4. Deep-link / file-open event example (warm case handled in Rust,
// cold case may pass initial url via payload).
export async function handleOpenedUrls(urls) {
  console.log("opened urls:", urls);
}
