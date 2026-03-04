import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import CollapsibleItem from "../CollapsibleItem.vue";

test("CollapsibleItem should toggle state when title is clicked", async () => {
  const wrapper = shallowMount(CollapsibleItem, {
    props: { initialState: false },
    slots: { title: "Title", content: "Content" },
  });

  expect(wrapper.text()).toContain("Title");
  expect(wrapper.text()).not.toContain("Content");

  await wrapper.find(".card-title").trigger("click");
  expect(wrapper.text()).toContain("Content");

  await wrapper.find(".card-title").trigger("click");
  expect(wrapper.text()).not.toContain("Content");
});

test("CollapsibleItem should be initially open if initialState is true", async () => {
  const wrapper = shallowMount(CollapsibleItem, {
    props: { initialState: true },
    slots: { title: "Title", content: "Content" },
  });

  expect(wrapper.text()).toContain("Content");
});
