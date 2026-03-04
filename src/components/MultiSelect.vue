<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";

import { useClickOutside } from "@/composables/click-outside.ts";

const model = defineModel<string[]>({ default: () => [] });

defineProps<{
  options?: { label: string; value: string }[];
  placeholder?: string;
  selectClass?: string;
}>();

const { t } = useI18n();

const isOpen = ref(false);
const elRef = ref<HTMLElement>();

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

useClickOutside(elRef, () => (isOpen.value = false));

const isSelected = (value: string) => model.value.includes(value);

const toggleOption = (value: string) => {
  if (isSelected(value)) {
    model.value = model.value.filter((v) => v !== value);
  } else {
    model.value = [...model.value, value];
  }
};
</script>

<template>
  <div
    ref="elRef"
    class="multi-select relative"
  >
    <span
      class="flex flex-row items-center select"
      :class="selectClass || ''"
      @click="toggleDropdown"
    >
      {{ placeholder || t("select.options") }}
      <span
        v-if="!!model.length"
        class="badge ml-1 p-1"
        >{{ model.length }}</span
      >
    </span>
    <div
      v-show="isOpen"
      class="absolute w-auto z-50 bg-base-100 border border-base-content/20 rounded-md shadow-lg max-h-60 overflow-y-auto right-0"
    >
      <ul class="p-2">
        <li
          v-for="option in options"
          :key="option.value"
          class="flex items-center gap-2 p-2 hover:bg-base-200 rounded-md cursor-pointer transition-colors"
          @click="toggleOption(option.value)"
        >
          <input
            type="checkbox"
            :checked="isSelected(option.value)"
            class="checkbox checkbox-primary checkbox-sm pointer-events-none"
          />
          <span class="grow">{{ option.label }}</span>
        </li>
        <li
          v-if="!options || options.length === 0"
          class="p-2 text-center text-base-content/50"
        >
          {{ t("select.no_options_available") }}
        </li>
      </ul>
    </div>
  </div>
</template>
