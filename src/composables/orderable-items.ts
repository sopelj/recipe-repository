import { computed, type Ref } from "vue";

import { OrderableItem } from "@/types/common";

export const reorderItems = <T extends OrderableItem>(items: T[]): T[] => {
  let order = 0;
  const newItems: T[] = [];
  const tempItems = [...items];
  tempItems.forEach((item: OrderableItem) => {
    if (item?.deleted !== true) {
      order += 1;
    }
    newItems.push({ ...item, order } as T);
  });
  return newItems;
};

export const useOrderableItems = <T extends OrderableItem>(items: Ref<T[]>, emptyItem: T) => {
  const visibleItems = computed((): T[] => items.value.filter((i: T) => i?.deleted !== true));

  const addItem = (): void => {
    items.value.push({
      ...emptyItem,
      order: visibleItems.value.length + 1,
    });
  };

  const deleteItem = (item: T): void => {
    let allItems = [...items.value];
    if (item.id) {
      item.deleted = true;
    } else if (!item.id && item.order == item.order) {
      allItems = allItems.filter((i: T) => i.order !== i.order);
    }
    items.value = reorderItems<T>(allItems);
  };

  return { addItem, deleteItem };
};
