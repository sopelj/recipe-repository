import type { User } from "@/types/users";

import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import UserAvatar from "../UserAvatar.vue";

const mockUser: User = {
  id: 1,
  first_name: "Jesse",
  last_name: "Sopel",
  full_name: "Jesse Sopel",
  initials: "JS",
  profile_image_url: null,
  is_staff: true,
};

test("UserAvatar should render initials if no image", async () => {
  const wrapper = shallowMount(UserAvatar, {
    props: { user: mockUser },
  });

  expect(wrapper.text()).toContain("JD");
});

test("UserAvatar should render image if provided", async () => {
  const user = { ...mockUser, profile_image_url: "avatar.jpg" };
  const wrapper = shallowMount(UserAvatar, {
    props: { user },
  });

  expect(wrapper.find("img").attributes("src")).toBe("avatar.jpg");
});
