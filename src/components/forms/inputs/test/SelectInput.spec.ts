import { mount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import SelectInput from "../SelectInput.vue";

vi.mock("@/composables/click-outside.ts", () => ({
  useClickOutside: vi.fn(),
}));

test("SelectInput should filter options by search term", async () => {
  const options = [
    { id: 1, name: "Apple" },
    { id: 2, name: "Banana" },
    { id: 3, name: "Cherry" },
  ];
  const wrapper = mount(SelectInput, {
    props: {
      id: "test-select",
      options,
      labelKey: "name",
      modelValue: null,
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  // Open the dropdown
  await wrapper.find(".select").trigger("click");

  // Initially all options should be visible (3 options + possibly a "no options" or search input)
  // Let's check for specific text
  expect(wrapper.text()).toContain("Apple");
  expect(wrapper.text()).toContain("Banana");
  expect(wrapper.text()).toContain("Cherry");

  // Search for "Ba"
  const searchInput = wrapper.find('input[type="text"]');
  await searchInput.setValue("Ba");

  // Only Banana should be visible
  expect(wrapper.text()).not.toContain("Apple");
  expect(wrapper.text()).toContain("Banana");
  expect(wrapper.text()).not.toContain("Cherry");
});

test("SelectInput should select an option", async () => {
  const options = [
    { id: 1, name: "Apple" },
    { id: 2, name: "Banana" },
  ];
  const wrapper = mount(SelectInput, {
    props: {
      id: "test-select",
      options,
      labelKey: "name",
      modelValue: null,
      "update:modelValue": (val: number | null) => wrapper.setProps({ modelValue: val }),
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  // Open dropdown
  await wrapper.find(".select").trigger("click");

  // Click on Banana
  const bananaOption = wrapper.findAll("li").find((li) => li.text().includes("Banana"));
  await bananaOption?.trigger("click");

  // Check if modelValue updated
  expect(wrapper.emitted()["update:modelValue"][0]).toEqual([2]);

  // Dropdown should be closed (isOpen should be false)
  // Since we use v-show for dropdown, we check if it's visible
  // const dropdown = wrapper.find(".absolute");
  await wrapper.vm.$nextTick();
  expect(wrapper.vm?.isOpen).toBe(false);
  // expect(dropdown.isVisible()).toBe(false);
});

test("SelectInput should focus search input when dropdown is opened", async () => {
  const options = [{ id: 1, name: "Apple" }];
  const wrapper = mount(SelectInput, {
    props: {
      id: "test-select",
      options,
      labelKey: "name",
      modelValue: null,
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
    attachTo: document.body, // Needed for focus testing
  });

  const searchInput = wrapper.find('input[type="text"]').element as HTMLInputElement;
  const spy = vi.spyOn(searchInput, "focus");

  // Open the dropdown
  await wrapper.find(".select").trigger("click");

  expect(spy).toHaveBeenCalled();
  wrapper.unmount();
});
