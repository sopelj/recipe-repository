import { afterEach } from "vitest";

import { i18n } from "@/plugins/i18n.ts";
import { formatDuration, formatISOTime, formatLocalised } from "../durations";

describe("formatDuration", () => {
  it("should only display non-zero values", () => {
    expect(formatDuration("10:00:10")).toMatch("10h10s");
    expect(formatDuration("00:01:50")).toMatch("1m50s");
  });
});

describe("formatLocalised", () => {
  afterEach(() => {
    i18n.global.locale.value = "en";
  });

  it("should translate Japanese", () => {
    i18n.global.locale.value = "ja";
    expect(formatLocalised("10:00:10")).toMatch("10時間10秒");
    expect(formatLocalised("00:01:50")).toMatch("1分50秒");
  });
});

describe("formatISOTime", () => {
  it("should properly convert to ISO", () => {
    expect(formatISOTime("10:00:10")).toMatch("PT10H10S");
    expect(formatISOTime("00:01:50")).toMatch("PT1M50S");
  });
});
