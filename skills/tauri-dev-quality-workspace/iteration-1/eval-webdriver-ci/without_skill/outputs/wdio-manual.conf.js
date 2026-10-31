import { spawn } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const appBinary = path.join(
  __dirname,
  '..',
  'src-tauri',
  'target',
  'release',
  os.platform() === 'win32' ? 'my-tauri-app.exe' : 'my-tauri-app'
);

const DRIVER_HOST = '127.0.0.1';
const DRIVER_PORT = 4444;

let driverProcess;

// Variante manuelle Windows / Linux :
// 1. On spawne `tauri-driver --port 4444` nous-mêmes (doit être dans le PATH :
//    `cargo install tauri-driver --locked`).
// 2. WDIO se connecte en client brut sur 127.0.0.1:4444 (pas de service `tauri`).
// 3. onAfterSession / onComplete tue le driver.
// Alternative 100% manuelle (debug) : lancer `tauri-driver --port 4444` dans un
// terminal séparé et commenter onBeforeSession ci-dessous.

export const config = {
  runner: 'local',
  specs: ['./test/specs/**/*.js'],
  exclude: [],
  maxInstances: 1,
  logLevel: 'info',
  bail: 0,
  waitforTimeout: 10000,
  connectionRetryTimeout: 120000,
  connectionRetryCount: 3,
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: {
    ui: 'bdd',
    timeout: 60000,
  },

  // Pas de `services: ['tauri']` ici : connexion directe au driver déjà en écoute.
  hostname: DRIVER_HOST,
  port: DRIVER_PORT,
  path: '/',
  protocol: 'http',

  capabilities: [
    {
      maxInstances: 1,
      browserName: 'wry',
      // Extension propriétaire Tauri : désigne le binaire applicatif à piloter.
      'tauri:options': {
        application: appBinary,
      },
    },
  ],

  onBeforeSession() {
    // Windows : tauri-driver.exe doit être dans le PATH (cargo bin dir).
    // Linux : idem + WebKitWebDriver requis côté système (voir CI).
    driverProcess = spawn('tauri-driver', ['--port', String(DRIVER_PORT)], {
      stdio: 'inherit',
      shell: os.platform() === 'win32',
    });
    driverProcess.on('error', (err) => {
      throw new Error(`Impossible de lancer tauri-driver: ${err.message}`);
    });
    // Laisse le temps au driver d'ouvrir le port avant la première session.
    return new Promise((resolve) => setTimeout(resolve, 2000));
  },

  onAfterSession() {
    driverProcess?.kill();
  },

  onComplete() {
    driverProcess?.kill();
  },
};
