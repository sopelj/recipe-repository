import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import ServingsForm from "../ServingsForm.vue";

vi.mock("@inertiajs/vue3", () => ({
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  useForm: (initialValues: any) => ({
    get: vi.fn(),
    processing: false,
    errors: {},
    servings: initialValues.servings,
  }),
}));

test("ServingsForm should render with initial servings", async () => {
  const wrapper = shallowMount(ServingsForm, {
    props: { servings: 4 },
  });

  expect(wrapper.find("input").element.value).toBe("4");
});
