import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import MultiSelect from "../MultiSelect.vue";

vi.mock("@/composables/click-outside.ts", () => ({
  useClickOutside: vi.fn(),
}));

test("MultiSelect should display placeholder and options", async () => {
  const options = [{ label: "Option 1", value: "1" }];
  const wrapper = shallowMount(MultiSelect, {
    props: { options, placeholder: "Select items" },
  });

  expect(wrapper.text()).toContain("Select items");

  await wrapper.find(".select").trigger("click");
  expect(wrapper.text()).toContain("Option 1");
});

test("MultiSelect should toggle options", async () => {
  const options = [{ label: "Option 1", value: "1" }];
  const wrapper = shallowMount(MultiSelect, {
    props: {
      options,
      modelValue: [],
      "onUpdate:modelValue": (val: string[]) => wrapper.setProps({ modelValue: val }),
    },
  });

  await wrapper.find(".select").trigger("click");
  await wrapper.find("li").trigger("click");

  expect(wrapper.vm.modelValue).toContain("1");
});
