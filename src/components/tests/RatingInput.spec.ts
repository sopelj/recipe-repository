import { shallowMount } from "@vue/test-utils";
import { expect, test } from "vitest";

import RatingInput from "../RatingInput.vue";

test("RatingInput should render stars", async () => {
  const wrapper = shallowMount(RatingInput, {
    props: { modelValue: 3 },
  });

  const stars = wrapper.findAll("button");
  expect(stars.length).toBe(5);

  const filledStars = wrapper.findAll(".icon-\\[tabler--star-filled\\]");
  expect(filledStars.length).toBe(3);
});

test("RatingInput should update value when star is clicked", async () => {
  const wrapper = shallowMount(RatingInput, {
    props: { modelValue: 0 },
  });

  await wrapper.findAll("button")[3].trigger("click");
  const events = wrapper.emitted("update:modelValue");
  expect(events).toBeDefined();
  expect(events?.length).toBe(1);
  if (!events) {
    throw Error("Not events returned");
  }
  expect(events[0]).toEqual([4]);
});
