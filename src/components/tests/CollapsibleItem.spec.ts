import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import CollapsibleItem from "../CollapsibleItem.vue";

it.todo("Test for height or visibility");

test("CollapsibleItem should toggle state when title is clicked", async () => {
  const wrapper = shallowMount(CollapsibleItem, {
    props: { initialState: false },
    slots: { title: "Title", content: "Content" },
  });
  expect(wrapper.text()).toContain("Title");
});

test("CollapsibleItem should be initially open if initialState is true", async () => {
  const wrapper = shallowMount(CollapsibleItem, {
    props: { initialState: true },
    slots: { title: "Title", content: "Content" },
  });

  expect(wrapper.text()).toContain("Content");
});
