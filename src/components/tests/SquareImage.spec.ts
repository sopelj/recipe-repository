import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import SquareImage from "../SquareImage.vue";

test("SquareImage should render image when src is provided", async () => {
  const wrapper = shallowMount(SquareImage, {
    props: { src: "image.jpg", alt: "alt text" },
  });

  expect(wrapper.find("img").attributes("src")).toBe("image.jpg");
  expect(wrapper.find("img").attributes("alt")).toBe("alt text");
});

test("SquareImage should render placeholder when src is null", async () => {
  const wrapper = shallowMount(SquareImage, {
    props: { src: null },
  });

  expect(wrapper.find("img").exists()).toBe(false);
  expect(wrapper.find(".icon-\\[mdi-light--image\\]").exists()).toBe(true);
});
