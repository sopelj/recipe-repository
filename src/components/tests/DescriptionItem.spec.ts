import { shallowMount } from "@vue/test-utils";

import DescriptionItem from "../DescriptionItem.vue";

test("Description Item should display label and content", async () => {
  const wrapper = shallowMount(DescriptionItem, { props: { label: "Label" }, slots: { default: "Content" } });
  expect(wrapper.text()).toContain("Label");
  expect(wrapper.text()).toContain("Content");
});
