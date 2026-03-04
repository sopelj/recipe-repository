<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  initialState?: boolean;
}>();

const isOpen = ref<boolean>(props.initialState ?? false);

const toggle = (): void => {
  isOpen.value = !isOpen.value;
};
</script>

<template>
  <div class="card p-2">
    <div
      class="card-title select-none cursor-pointer flex flex-row items-center"
      @click="toggle"
    >
      <div class="grow">
        <slot name="title" />
      </div>
      <span
        class="icon-[tabler--chevron-down] size-5 transition-transform duration-300"
        :class="{ 'rotate-180': isOpen }"
      ></span>
    </div>
    <div
      class="card-body overflow-hidden transition-[max-height] duration-300"
      :class="isOpen ? 'max-h-200' : 'max-h-0'"
    >
      <div class="pt-2">
        <slot name="content" />
      </div>
    </div>
  </div>
</template>
