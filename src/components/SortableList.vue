<script setup lang="ts" generic="T extends OrderableItem">
import type { OrderableItem } from "@/types/common";

import { computed, ref } from "vue";

import { reorderItems } from "@/composables/orderable-items";

const items = defineModel<T[]>({ required: true });
const props = withDefaults(defineProps<{ rowClass?: string }>(), { rowClass: "" });

const dragSourceIndex = ref<number | null>(null);
const dragTargetIndex = ref<number | null>(null);

const onDragStart = (event: DragEvent, index: number) => {
  dragSourceIndex.value = index;
  if (event.dataTransfer) {
    event.dataTransfer.setData("text/plain", index.toString());
    event.dataTransfer.dropEffect = "move";
  }
};

const onDragOver = (event: DragEvent) => {
  event.preventDefault();
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = "move";
  }
};

const onDragEnter = (index: number) => {
  dragTargetIndex.value = index;
};

const onDragLeave = (index: number) => {
  if (dragTargetIndex.value === index) {
    dragTargetIndex.value = null;
  }
};

const onDragEnd = () => {
  dragSourceIndex.value = null;
  dragTargetIndex.value = null;
};

const onDrop = (event: DragEvent, toIndex: number) => {
  event.preventDefault();
  const fromIndex = parseInt(event.dataTransfer?.getData("text/plain") || "-1");

  dragSourceIndex.value = null;
  dragTargetIndex.value = null;

  if (fromIndex !== -1 && fromIndex !== toIndex) {
    const tempItems = [...items.value];
    const [movedItem] = tempItems.splice(fromIndex, 1);
    tempItems.splice(toIndex, 0, movedItem);
    items.value = reorderItems<T>(tempItems);
  }
};

const rowClasses = computed(() =>
  props.rowClass.split(" ").reduce((acc, part) => (part ? { ...acc, [part]: true } : acc), {}),
);
</script>

<template>
  <div class="grid grid-flow-row gap-2">
    <div
      v-if="$slots.header"
      :class="rowClasses"
    >
      <slot name="header"></slot>
    </div>
    <template
      v-for="(item, index) in items"
      :key="index"
    >
      <div
        v-if="item?.deleted !== true"
        draggable="true"
        class="transition-all duration-200"
        :class="{
          'border-t-2 border-primary pt-2':
            dragTargetIndex === index && dragTargetIndex <= (dragSourceIndex || 0),
          'border-b-2 border-primary pb-2':
            dragTargetIndex === index && dragTargetIndex > (dragSourceIndex || 0),
          'opacity-50': dragSourceIndex === index,
          ...rowClasses,
        }"
        @dragstart="onDragStart($event, index)"
        @dragover="onDragOver($event)"
        @dragenter="onDragEnter(index)"
        @dragleave="onDragLeave(index)"
        @dragend="onDragEnd"
        @drop="onDrop($event, index)"
      >
        <slot
          :item="item"
          :index="index"
        />
      </div>
    </template>
    <div
      v-if="$slots.footer"
      :class="rowClasses"
    >
      <slot name="footer"></slot>
    </div>
  </div>
</template>
