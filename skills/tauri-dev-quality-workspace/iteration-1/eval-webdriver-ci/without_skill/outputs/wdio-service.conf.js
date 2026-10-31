import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Binaire Tauri v2 à tester (build release préalable requis)
const appBinary = path.join(
  __dirname,
  '..',
  'src-tauri',
  'target',
  'release',
  os.platform() === 'win32' ? 'my-tauri-app.exe' : 'my-tauri-app'
);

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

  // Service embarqué : wdio lance et arrête tauri-driver tout seul.
  // Prérequis npm : @wdio/cli, @wdio/local-runner, @wdio/mocha-framework,
  // @wdio/spec-reporter, tauri-driver (cargo install tauri-driver --locked),
  // + le service WDIO `tauri` (npm i -D wdio-tauri-service).
  services: [
    [
      'tauri',
      {
        // Chemin du binaire applicatif passé à tauri-driver
        application: appBinary,
        // Mode embedded : pas besoin de `tauri-driver` lancé à la main
        // ni de hostname/port dans cette variante.
      },
    ],
  ],

  capabilities: [
    {
      maxInstances: 1,
      // tauri-driver parle WRY/WebView, pas Chrome/Firefox.
      browserName: 'wry',
      'tauri:options': {
        application: appBinary,
      },
    },
  ],
};
