import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";

import SortableList from "../SortableList.vue";

test("SortableList should render items via slot", () => {
  const items = [
    { id: 1, name: "Item 1", order: 1 },
    { id: 2, name: "Item 2", order: 2 },
  ];
  const wrapper = mount(SortableList, {
    props: { modelValue: items },
    slots: {
      default: `<template #default="{ item }"><span>{{ item.name }}</span></template>`,
    },
  });

  expect(wrapper.text()).toContain("Item 1");
  expect(wrapper.text()).toContain("Item 2");
  expect(wrapper.findAll('[draggable="true"]')).toHaveLength(2);
});

test("SortableList should emit update:modelValue on drop", async () => {
  const items = [
    { id: 1, name: "Item 1", order: 1 },
    { id: 2, name: "Item 2", order: 2 },
  ];
  const wrapper = mount(SortableList, {
    props: { modelValue: items },
  });

  const draggableItems = wrapper.findAll('[draggable="true"]');

  // Mock dataTransfer
  const dataTransfer = {
    setData: (type: string, val: string) => {
      dataTransfer.data[type] = val;
    },
    getData: (type: string) => dataTransfer.data[type],
    data: {} as Record<string, string>,
    dropEffect: "",
  };

  // Drag first item to second position
  await draggableItems[0].trigger("dragstart", { dataTransfer });
  expect(dataTransfer.data["text/plain"]).toBe("0");

  await draggableItems[1].trigger("drop", {
    dataTransfer,
    preventDefault: () => {},
  });

  const emitted = wrapper.emitted("update:modelValue");
  expect(emitted).toBeTruthy();
  const updatedItems = emitted![0][0] as typeof items;
  expect(updatedItems[0].id).toBe(2);
  expect(updatedItems[1].id).toBe(1);
  expect(updatedItems[0].order).toBe(1);
  expect(updatedItems[1].order).toBe(2);
});
