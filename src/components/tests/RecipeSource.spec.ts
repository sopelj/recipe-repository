import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import RecipeSource from "../RecipeSource.vue";

test("RecipeSource should render website source", async () => {
  const source = { name: "Tasty", type: 1 as const };
  const wrapper = shallowMount(RecipeSource, {
    props: { source, value: "https://example.com" },
  });

  expect(wrapper.find("a").attributes("href")).toBe("https://example.com");
  expect(wrapper.text()).toContain("Tasty");
});

test("RecipeSource should render book source", async () => {
  const source = { name: "Cookbook", type: 2 as const, value: "133-23145" };
  const wrapper = shallowMount(RecipeSource, {
    props: { source, value: "10" },
  });

  expect(wrapper.text()).toContain("Cookbook, p.10");
});
