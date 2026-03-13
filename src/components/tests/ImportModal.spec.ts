import { mount, shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import ImportModal from "../ImportModal.vue";

const mockForm = {
  url: "",
  post: vi.fn(),
  resetAndClearErrors: vi.fn(),
  processing: false,
  errors: {},
};

vi.mock("@inertiajs/vue3", () => ({
  useForm: () => mockForm,
}));

test("ImportModal should render when open", async () => {
  const wrapper = shallowMount(ImportModal, {
    props: {
      modelValue: true,
      "update:modelValue": (val: boolean) => wrapper.setProps({ modelValue: val }),
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  expect(wrapper.find('[role="dialog"]').exists()).toBe(true);
  expect(wrapper.text()).toContain("recipe.import");
});

test("ImportModal should call post on submit", async () => {
  const wrapper = mount(ImportModal, {
    props: {
      modelValue: true,
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  const input = wrapper.find('input[type="url"]');
  await input.setValue("https://example.com/recipe");

  // Wait for model update
  mockForm.url = "https://example.com/recipe";

  await wrapper.find("form").trigger("submit.prevent");
  expect(mockForm.post).toHaveBeenCalled();
});

test("ImportModal should close on button click", async () => {
  const wrapper = mount(ImportModal, {
    props: {
      modelValue: true,
      "update:modelValue": (val: boolean) => wrapper.setProps({ modelValue: val }),
    },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  await wrapper.find('button[aria-label="Close"]').trigger("click");

  expect(wrapper.emitted()["update:modelValue"][0]).toEqual([false]);
  expect(mockForm.resetAndClearErrors).toHaveBeenCalled();
});
