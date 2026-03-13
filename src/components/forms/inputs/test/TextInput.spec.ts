import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import TextInput from "../TextInput.vue";

test("TextInput should render with label and value", async () => {
  const wrapper = mount(TextInput, {
    props: {
      id: "test-textarea",
      label: "Test Label",
      modelValue: "initial text",
    },
  });

  expect(wrapper.find("label").text()).toBe("Test Label");
  const textarea = wrapper.find("textarea");
  expect((textarea.element as HTMLTextAreaElement).value).toBe("initial text");
});

test("TextInput should update modelValue on input", async () => {
  const wrapper = mount(TextInput, {
    props: {
      id: "test-textarea",
      modelValue: "",
      "update:modelValue": (val: string) => wrapper.setProps({ modelValue: val }),
    },
  });

  const textarea = wrapper.find("textarea");
  await textarea.setValue("new text");
  expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["new text"]);
});

test("TextInput should display errors", () => {
  const wrapper = mount(TextInput, {
    props: {
      id: "test-textarea",
      errors: ["Error 1"],
    },
  });

  const errors = wrapper.findAll("li");
  expect(errors).toHaveLength(1);
  expect(errors[0].text()).toBe("Error 1");
  expect(wrapper.find("textarea").classes()).toContain("is-invalid");
});

test("TextInput should use placeholder", () => {
  const wrapper = mount(TextInput, {
    props: {
      id: "test-textarea",
      placeholder: "Enter some text",
    },
  });

  const textarea = wrapper.find("textarea");
  expect(textarea.attributes("placeholder")).toBe("Enter some text");
});
