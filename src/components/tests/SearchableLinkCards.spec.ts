import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import SearchableLinkCards from "../SearchableLinkCards.vue";

test("SearchableLinkCards should display items", async () => {
  const gridItems = [{ name: "Item 1", slug: "item-1", thumbnail_url: "" }];
  const wrapper = shallowMount(SearchableLinkCards, {
    props: {
      gridItems,
      routeName: "category_detail",
      type: "category",
      noResultsMessage: "No items",
    },
    global: {
      stubs: {
        Link: {
          template: "<a><slot /></a>",
        },
        "square-image": true,
      },
    },
  });

  expect(wrapper.text()).toContain("Item 1");
});

test("SearchableLinkCards should display no results message", async () => {
  const wrapper = shallowMount(SearchableLinkCards, {
    props: {
      gridItems: [],
      routeName: "category_detail",
      type: "category",
      noResultsMessage: "No items found",
    },
  });

  expect(wrapper.text()).toContain("No items found");
});
