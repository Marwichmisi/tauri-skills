// Tiré de develop/Tests/WebDriver/index.mdx (route service recommandée).
// Variantes doc : driverProvider 'embedded' (défaut, macOS OK via
// tauri-plugin-wdio-webdriver) | 'external' | 'crabnebula' (clé API payante).
export const config = {
  services: [
    [
      "tauri",
      {
        appBinaryPath: "./src-tauri/target/release/my-tauri-app",
        driverProvider: "embedded",
      },
    ],
  ],
};
