import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import RatingForm from "../RatingForm.vue";

vi.mock("@inertiajs/vue3", () => ({
  useForm: () => ({
    post: vi.fn(),
    processing: false,
    errors: {},
    clearErrors: vi.fn(),
    rating: 0,
  }),
}));

vi.mock("vue-toastification", () => ({
  useToast: () => ({
    error: vi.fn(),
  }),
}));

test("RatingForm should render", async () => {
  const wrapper = shallowMount(RatingForm, {
    props: { numRatings: 5, userRating: 4, averageRating: 3.5 },
  });
  expect(wrapper.findComponent({ name: "RatingInput" })).toBeDefined();
});
