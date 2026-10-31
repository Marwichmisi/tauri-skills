// mock-test.js — Test frontend Vitest : mock commande 'add' (12+15=27)
// Contexte : Tauri v2 frontend, jsdom + WebCrypto shim, espions invoke, fenêtres main/second/third

// --- Shim WebCrypto pour jsdom (inclus, requis car jsdom n'expose pas webcrypto) ---
import { webcrypto } from 'node:crypto';
if (typeof globalThis.crypto === 'undefined' || !globalThis.crypto.subtle) {
  Object.defineProperty(globalThis, 'crypto', {
    value: webcrypto,
    configurable: true,
    writable: true,
  });
}

import { describe, it, expect, vi, afterEach, beforeEach } from 'vitest';

// --- Mocks Tauri API ---
// Espion invoke : intercepte la commande 'add'
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}));

// Mock fenêtres main / second / third
vi.mock('@tauri-apps/api/webviewWindow', () => {
  const makeWin = (label) => ({
    label,
    close: vi.fn(),
    show: vi.fn(),
    hide: vi.fn(),
  });
  return {
    WebviewWindow: vi.fn().mockImplementation((label) => makeWin(label)),
    getAllWebviewWindows: vi.fn().mockResolvedValue([
      makeWin('main'),
      makeWin('second'),
      makeWin('third'),
    ]),
    getCurrentWebviewWindow: vi.fn().mockReturnValue(makeWin('main')),
  };
});

import { invoke } from '@tauri-apps/api/core';
import {
  getAllWebviewWindows,
  getCurrentWebviewWindow,
} from '@tauri-apps/api/webviewWindow';

// --- Code frontend sous test (exemple minimal) ---
async function add(a, b) {
  return await invoke('add', { a, b });
}

async function listWindowLabels() {
  const wins = await getAllWebviewWindows();
  return wins.map((w) => w.label);
}

describe('frontend mock: commande add + fenêtres', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Mock commande 'add' : 12 + 15 = 27
    invoke.mockImplementation((cmd, args) => {
      if (cmd === 'add') {
        const { a, b } = args;
        if (a === 12 && b === 15) return Promise.resolve(27);
        return Promise.resolve(a + b);
      }
      return Promise.reject(new Error(`commande inconnue: ${cmd}`));
    });
  });

  // Clear les mocks après chaque run
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("mocke la commande 'add' : 12+15=27 avec espion invoke", async () => {
    const result = await add(12, 15);

    expect(result).toBe(27);
    // Vérifie l'espion invoke : appelé 1 fois avec ('add', {a:12,b:15})
    expect(invoke).toHaveBeenCalledTimes(1);
    expect(invoke).toHaveBeenCalledWith('add', { a: 12, b: 15 });
  });

  it('mocke les fenêtres main / second / third', async () => {
    const labels = await listWindowLabels();

    expect(labels).toEqual(['main', 'second', 'third']);
    expect(getAllWebviewWindows).toHaveBeenCalledTimes(1);

    const current = getCurrentWebviewWindow();
    expect(current.label).toBe('main');
  });

  it('clear les mocks après chaque run (invoke repart à zéro)', async () => {
    // Grâce à clearAllMocks dans beforeEach/afterEach, l'espion est vide ici
    expect(invoke).not.toHaveBeenCalled();

    await add(12, 15);
    expect(invoke).toHaveBeenCalledTimes(1);
    // Le afterEach suivant fera clearAllMocks() automatiquement
  });
});
