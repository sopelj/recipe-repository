import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import BreadcrumbBar from "../BreadcrumbBar.vue";

test("BreadcrumbBar should display home and items", async () => {
  const items = [{ label: "Category", url: "/category" }];
  const current = "Recipe";
  const wrapper = shallowMount(BreadcrumbBar, {
    props: { items, current },
    global: {
      stubs: {
        Link: {
          template: "<a><slot /></a>",
        },
      },
    },
  });

  expect(wrapper.text()).toContain("Category");
  expect(wrapper.text()).toContain("Recipe");
});
