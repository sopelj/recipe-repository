import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import InputField from "../InputField.vue";

test("InputField should render with label and value", async () => {
  const wrapper = mount(InputField, {
    props: {
      id: "test-input",
      label: "Test Label",
      modelValue: "initial value",
    },
  });

  expect(wrapper.find("label").text()).toBe("Test Label");
  const input = wrapper.find("input");
  expect((input.element as HTMLInputElement).value).toBe("initial value");
});

test("InputField should update modelValue on input", async () => {
  const wrapper = mount(InputField, {
    props: {
      id: "test-input",
      modelValue: "",
      "update:modelValue": (val: string) => wrapper.setProps({ modelValue: val }),
    },
  });

  const input = wrapper.find("input");
  await input.setValue("new value");
  expect(wrapper.emitted()["update:modelValue"][0]).toEqual(["new value"]);
});

test("InputField should display errors", () => {
  const wrapper = mount(InputField, {
    props: {
      id: "test-input",
      errors: ["Error 1", "Error 2"],
    },
  });

  const errors = wrapper.findAll("li");
  expect(errors).toHaveLength(2);
  expect(errors[0].text()).toBe("Error 1");
  expect(errors[1].text()).toBe("Error 2");
  expect(wrapper.find("input").classes()).toContain("is-invalid");
});

test("InputField should use correct type and placeholder", () => {
  const wrapper = mount(InputField, {
    props: {
      id: "test-input",
      type: "password",
      placeholder: "Enter password",
    },
  });

  const input = wrapper.find("input");
  expect(input.attributes("type")).toBe("password");
  expect(input.attributes("placeholder")).toBe("Enter password");
});
