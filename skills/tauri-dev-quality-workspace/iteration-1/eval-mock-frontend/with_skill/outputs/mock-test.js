import { mockIPC, mockWindows, clearMocks } from "@tauri-apps/api/mocks";
import { invoke } from "@tauri-apps/api/core";
import { afterEach, expect, test, vi } from "vitest";

// jsdom doesn't come with a WebCrypto implementation (develop/Tests/mocking.mdx)
import { randomFillSync } from "crypto";
import { beforeAll } from "vitest";

beforeAll(() => {
  Object.defineProperty(window, "crypto", {
    value: {
      // @ts-ignore
      getRandomValues: (buffer) => {
        return randomFillSync(buffer);
      },
    },
  });
});

afterEach(() => {
  clearMocks();
});

test("invoke simple", async () => {
  mockIPC((cmd, args) => {
    // simulated rust command called "add" that just adds two numbers
    if (cmd === "add") {
      return args.a + args.b;
    }
  });

  // we can use the spying tools provided by vitest to track the mocked function
  const spy = vi.spyOn(window.__TAURI_INTERNALS__, "invoke");

  expect(invoke("add", { a: 12, b: 15 })).resolves.toBe(27);
  expect(spy).toHaveBeenCalled();
});

test("windows", async () => {
  mockWindows("main", "second", "third");

  const { getCurrent, getAll } = await import("@tauri-apps/api/webviewWindow");

  expect(getCurrent()).toHaveProperty("label", "main");
  expect(getAll().map((w) => w.label)).toEqual(["main", "second", "third"]);
});
