import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import NutritionalInformation from "../NutritionalInformation.vue";

test("NutritionalInformation should display nutrition facts", async () => {
  const nutrition = {
    calories: 100,
    serving_size: 2,
    fat: 5,
    protein: 10,
    carbohydrate: 20,
  };
  const wrapper = mount(NutritionalInformation, {
    props: { nutrition },
  });

  // It's wrapped in CollapsibleItem, which is closed by default.
  // We need to click to open it or check if the title is there.
  expect(wrapper.text()).toContain("Nutritional Information");

  await wrapper.find(".card-title").trigger("click");
  expect(wrapper.text()).toContain("100");
  expect(wrapper.text()).toContain("Fat");
});
