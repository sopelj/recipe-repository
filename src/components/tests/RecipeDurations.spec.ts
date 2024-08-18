import { mount } from "@vue/test-utils";
import RecipeDurations from "../RecipeDurations.vue";

test("Duration Splitter should be empty without a time", async () => {
  const wrapper = mount(RecipeDurations, { props: { type: "prep" } });
  expect(wrapper.text()).toMatch("");
});

test("Duration Splitter should display time", async () => {
  const wrapper = mount(
    RecipeDurations,
    { props: { cookTime: "00:05:01", prepTime: "00:02:01", totalTime: "00:07:02" } }
  );
  const prepMeta = wrapper.find("[data-duration-type=\"prepTime\"] meta");
  expect(prepMeta.attributes("itemprop")).toBe("prepTime");
  expect(prepMeta.attributes("content")).toBe("PT2M1S");

  const totalMeta = wrapper.find("[data-duration-type=\"prepTime\"] meta");
  expect(totalMeta.attributes("itemprop")).toBe("prepTime");
  expect(totalMeta.attributes("content")).toBe("PT2M1S");

  expect(wrapper.text()).toBe("times.prepTime times.cookTime times.totalTime");
});
