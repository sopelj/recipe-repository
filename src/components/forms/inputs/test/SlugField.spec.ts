import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import SlugField from "../SlugField.vue";

test("SlugField should generate slug from sourceValue", async () => {
  const wrapper = mount(SlugField, {
    props: {
      id: "test-slug",
      sourceValue: "My Recipe",
      modelValue: "",
      "update:modelValue": (val: string) => wrapper.setProps({ modelValue: val }),
    },
  });

  // Initially modelValue is empty because watcher only triggers on change
  // Wait, the watcher triggers on props.sourceValue change.

  await wrapper.setProps({ sourceValue: "New Recipe Name" });
  expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["new-recipe-name"]);
});

test("SlugField should be readonly", () => {
  const wrapper = mount(SlugField, {
    props: {
      id: "test-slug",
      sourceValue: "",
    },
  });

  const input = wrapper.find("input");
  expect(input.attributes("readonly")).toBeDefined();
  expect(input.attributes("tabindex")).toBe("-1");
});

test("SlugField should display errors", () => {
  const wrapper = mount(SlugField, {
    props: {
      id: "test-slug",
      sourceValue: "",
      errors: ["Slug already exists"],
    },
  });

  expect(wrapper.find("li").text()).toBe("Slug already exists");
  expect(wrapper.find("input").classes()).toContain("is-invalid");
});
