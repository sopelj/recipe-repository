import type { Ingredient, IngredientGroup } from "@/types/recipes.ts";

import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import IngredientList from "../IngredientList.vue";

test("IngredientList should display ingredients", async () => {
  const ingredients: Ingredient[] = [
    {
      id: 1,
      food_display: "Sugar",
      amount_display: "100g",
      group_id: null,
      optional: false,
      note: "",
      qualifier: "",
    },
  ];
  const groups: IngredientGroup[] = [];
  const wrapper = mount(IngredientList, {
    props: { ingredients, groups },
  });

  expect(wrapper.text()).toContain("Sugar");
  expect(wrapper.text()).toContain("100g");
});

test("IngredientList should display grouped ingredients", async () => {
  const ingredients: Ingredient[] = [
    {
      id: 1,
      food_display: "Sugar",
      amount_display: "100g",
      group_id: 1,
      optional: false,
      note: "",
      qualifier: "",
    },
  ];
  const groups: IngredientGroup[] = [{ id: 1, name: "Main", order: 0 }];
  const wrapper = mount(IngredientList, {
    props: { ingredients, groups },
  });

  expect(wrapper.text()).toContain("Main");
  expect(wrapper.text()).toContain("Sugar");
});
