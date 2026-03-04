import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import KeepAwake from "../KeepAwake.vue";

afterAll(() => {
  vi.unstubAllGlobals();
});

test("KeepAwake should render label", async () => {
  const wrapper = shallowMount(KeepAwake);
  expect(wrapper.text()).toContain("Keep screen on");
});

describe("KeepAwake in browser supporting wakeLock", () => {
  beforeAll(() => {
    vi.stubGlobal("navigator", { wakeLock: class WakeLock {} });
  });

  test("KeepAwake switch should enabled if wakeLock is supported", async () => {
    const wrapper = shallowMount(KeepAwake);
    const checkbox = wrapper.find('input[type="checkbox"]');

    expect(checkbox.attributes("disabled")).not.toBeDefined();
  });
});

describe("KeepAwake in browser not supporting wakeLock", () => {
  beforeAll(() => {
    vi.stubGlobal("navigator", {});
  });
  test("KeepAwake switch should be disabled if wakeLock is not supported", async () => {
    const wrapper = shallowMount(KeepAwake);
    const checkbox = wrapper.find('input[type="checkbox"]');
    expect(checkbox.attributes("disabled")).toBeDefined();
  });
});
