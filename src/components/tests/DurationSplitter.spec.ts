import { mount } from "@vue/test-utils";
import DurationSplitter from "../RecipeDurations.vue";

test("Duration Splitter should be empty without a time", async () => {
  const wrapper = mount(DurationSplitter, { props: { type: "prep" } });
  expect(wrapper.text()).toMatch("");
});

test("Duration Splitter should display time", async () => {
  const wrapper = mount(DurationSplitter, { props: { type: "prep", time: "00:05:01" } });
  const meta = wrapper.find("meta");
  expect(meta.attributes("itemprop")).toBe("prepTime");
  expect(meta.attributes("content")).toBe("PT5M1S");
  expect(wrapper.text()).toBe("times.prep 5m1s");
});
