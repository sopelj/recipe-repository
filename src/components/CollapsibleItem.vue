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
  <div class="card">
    <div
      class="card-title p-2 cursor-pointer flex flex-row items-center"
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
      v-if="isOpen"
      class="card-body p-2 overflow-hidden transition-[height] duration-300"
    >
      <slot name="content" />
    </div>
  </div>
</template>
