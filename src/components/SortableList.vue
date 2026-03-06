<script setup lang="ts" generic="T extends { order: number }">
import { ref } from "vue";

const props = defineProps<{ modelValue: T[] }>();

const emit = defineEmits<{ (e: "update:modelValue", value: T[]): void }>();

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
    const items = [...props.modelValue];
    const [movedItem] = items.splice(fromIndex, 1);
    items.splice(toIndex, 0, movedItem);

    // Update order property
    const updatedItems = items.map((item, index) => ({
      ...item,
      order: index + 1,
    }));

    emit("update:modelValue", updatedItems);
  }
};
</script>

<template>
  <div class="flex flex-col gap-2">
    <div
      v-for="(item, index) in modelValue"
      :key="index"
      draggable="true"
      class="transition-all duration-200"
      :class="{
        'border-t-2 border-primary pt-2':
          dragTargetIndex === index && dragTargetIndex <= (dragSourceIndex || 0),
        'border-b-2 border-primary pb-2':
          dragTargetIndex === index && dragTargetIndex > (dragSourceIndex || 0),
        'opacity-50': dragSourceIndex === index,
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
  </div>
</template>
