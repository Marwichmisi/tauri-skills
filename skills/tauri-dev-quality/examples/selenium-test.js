// Tiré de develop/Tests/WebDriver/Example/selenium.mdx (test/test.js, extrait).
// Route manuelle Windows/Linux seuls ; build --debug --no-bundle avant session.
import os from "os";
import path from "path";
import { expect } from "chai";
import { spawn, spawnSync } from "child_process";
import { Builder, By, Capabilities } from "selenium-webdriver";
import { fileURLToPath } from "url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));

// create the path to the expected application binary
const application = path.resolve(__dirname, "..", "..", "src-tauri", "target", "debug", "tauri-app");

let driver;
let tauriDriver;
let exit = false;

before(async function () {
  this.timeout(120000);
  spawnSync("yarn", ["tauri", "build", "--debug", "--no-bundle"], {
    cwd: path.resolve(__dirname, "../.."),
    stdio: "inherit",
    shell: true,
  });
  tauriDriver = spawn(path.resolve(os.homedir(), ".cargo", "bin", "tauri-driver"), [], {
    stdio: [null, process.stdout, process.stderr],
  });

  const capabilities = new Capabilities();
  capabilities.set("tauri:options", { application });
  capabilities.setBrowserName("wry");

  driver = await new Builder()
    .withCapabilities(capabilities)
    .usingServer("http://127.0.0.1:4444/")
    .build();
});

describe("Hello Tauri", () => {
  it("should be cordial", async () => {
    const text = await driver.findElement(By.css("body > h1")).getText();
    expect(text).to.match(/^[hH]ello/);
  });
});
