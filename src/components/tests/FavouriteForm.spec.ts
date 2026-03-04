import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import FavouriteForm from "../FavouriteForm.vue";

vi.mock("@inertiajs/vue3", () => ({
  useForm: () => ({
    post: vi.fn(),
    processing: false,
    errors: {},
    clearErrors: vi.fn(),
  }),
}));

vi.mock("vue-toastification", () => ({
  useToast: () => ({
    error: vi.fn(),
  }),
}));

test("FavouriteForm should render correctly based on userFavourite prop", async () => {
  const wrapperTrue = shallowMount(FavouriteForm, {
    props: { userFavourite: true },
  });
  expect(wrapperTrue.find(".icon-\\[mdi--heart\\]").exists()).toBe(true);

  const wrapperFalse = shallowMount(FavouriteForm, {
    props: { userFavourite: false },
  });
  expect(wrapperFalse.find(".icon-\\[mdi--heart-outline\\]").exists()).toBe(true);
});
