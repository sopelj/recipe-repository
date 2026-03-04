import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import RecipeYield from "../RecipeYield.vue";

test("RecipeYield should calculate and display yield", async () => {
  const unit = { name: "pie", name_plural: "pies" };
  const wrapper = shallowMount(RecipeYield, {
    props: { amount: 2, baseServings: 4, servings: 8, unit },
  });

  expect(wrapper.text()).toContain("4");
  expect(wrapper.text()).toContain("servings");
});
