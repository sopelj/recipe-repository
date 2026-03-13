import type { User } from "@/types/users";

import { shallowMount } from "@vue/test-utils";
import { expect, test, vi } from "vitest";

import UserMenu from "../UserMenu.vue";

vi.mock("@/composables/click-outside.ts", () => ({
  useClickOutside: vi.fn(),
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

test("UserMenu should toggle dropdown on click", async () => {
  const wrapper = shallowMount(UserMenu, {
    props: { user: mockUser },
    global: {
      mocks: {
        t: (key: string) => key,
      },
    },
  });

  // Dropdown should be closed initially
  expect(wrapper.find("ul").exists()).toBe(false);

  // Click on avatar
  await wrapper.findComponent({ name: "UserAvatar" }).trigger("click");
  expect(wrapper.find("ul").exists()).toBe(true);
  expect(wrapper.text()).toContain("global.admin");
  expect(wrapper.text()).toContain("global.logout");

  // Click again to close
  await wrapper.findComponent({ name: "UserAvatar" }).trigger("click");
  expect(wrapper.find("ul").exists()).toBe(false);
});
