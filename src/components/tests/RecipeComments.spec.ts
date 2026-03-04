import type { Comment } from "@/types/recipes";
import type { User } from "@/types/users";

import { mount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import RecipeComments from "../RecipeComments.vue";

vi.mock("@inertiajs/vue3", () => ({
  useForm: () => ({
    post: vi.fn(),
    reset: vi.fn(),
    comment: "",
  }),
}));

const mockUser: User = {
  id: 1,
  first_name: "Jesse",
  last_name: "Sopel",
  full_name: "Jesse Sopel",
  initials: "JS",
  profile_image_url: null,
  is_staff: true,
};

test("RecipeComments should render title and comment count", async () => {
  const comments: Comment[] = [{ created: "2023-01-01T00:00:00Z", text: "Nice!", user: mockUser }];
  const wrapper = mount(RecipeComments, {
    props: { comments },
  });

  expect(wrapper.text()).toContain("Comments");
  expect(wrapper.text()).toContain("1");
});

test("RecipeComments should show comments when opened", async () => {
  const comments: Comment[] = [{ created: "2023-01-01T00:00:00Z", text: "Nice!", user: mockUser }];
  const wrapper = mount(RecipeComments, {
    props: { comments },
  });

  await wrapper.find(".card-title").trigger("click");
  expect(wrapper.text()).toContain("Nice!");
});
