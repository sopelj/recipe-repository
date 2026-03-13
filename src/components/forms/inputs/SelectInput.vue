<script
  setup
  lang="ts"
  generic="T extends { id: number | null; name?: string; label?: string; text?: string }"
>
import { computed, nextTick, ref } from "vue";
import { useI18n } from "vue-i18n";

import { useClickOutside } from "@/composables/click-outside.ts";

interface Props {
  label?: string;
  id: string;
  options: T[];
  labelKey?: keyof T;
  errors?: string[] | string;
}

const model = defineModel<number | null>();
const props = withDefaults(defineProps<Props>(), {
  label: "",
  labelKey: "label" as keyof T,
  errors: () => [],
});

const { t } = useI18n();
const errorList = computed((): string[] => (Array.isArray(props.errors) ? props.errors : [props.errors]));

const isOpen = ref(false);
const searchTerm = ref("");
const elRef = ref<HTMLElement>();
const searchInput = ref<HTMLInputElement>();

const toggleDropdown = async () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    searchTerm.value = "";
    await nextTick();
    searchInput.value?.focus();
  }
};

useClickOutside(elRef, () => (isOpen.value = false));

const filteredOptions = computed(() => {
  if (!searchTerm.value) return props.options;
  return props.options.filter((option) => {
    const label = String(option[props.labelKey as keyof T] || "");
    return label.toLowerCase().includes(searchTerm.value.toLowerCase());
  });
});

const selectedLabel = computed(() => {
  const selected = props.options.find((option) => option.id === model.value);
  return selected ? String(selected[props.labelKey as keyof T]) : t("select.options");
});

const selectOption = (id: number | null) => {
  model.value = id;
  isOpen.value = false;
};
</script>

<template>
  <div
    ref="elRef"
    class="w-full relative"
  >
    <label
      v-if="label"
      class="label-text"
      :for="`${id}-input`"
    >
      {{ label }}
    </label>
    <div
      class="select flex items-center cursor-pointer min-h-10 px-4 truncate"
      :class="errors?.length ? 'is-invalid' : ''"
      @click="toggleDropdown"
    >
      <span class="truncate grow">
        {{ selectedLabel }}
      </span>
    </div>

    <div
      v-show="isOpen"
      class="absolute w-full z-50 bg-base-100 border border-base-content/20 rounded-md shadow-lg max-h-80 overflow-hidden flex flex-col"
    >
      <div class="p-2 border-b border-base-content/10">
        <input
          :id="`${id}-input`"
          ref="searchInput"
          v-model="searchTerm"
          type="text"
          class="input input-sm input-bordered w-full"
          :placeholder="t('search')"
          @click.stop
        />
      </div>
      <ul class="overflow-y-auto grow p-2">
        <li
          v-for="(option, i) in filteredOptions"
          :key="i"
          class="p-2 hover:bg-base-200 rounded-md cursor-pointer transition-colors"
          :class="model === option.id ? 'bg-base-300' : ''"
          @click="selectOption(option.id)"
        >
          <slot
            name="option"
            :option="option"
          >
            {{ option[labelKey as keyof T] }}
          </slot>
        </li>
        <li
          v-if="filteredOptions.length === 0"
          class="p-2 text-center text-base-content/50"
        >
          {{ t("no_results") }}
        </li>
      </ul>
    </div>

    <ul
      v-if="errorList.length"
      class="text-red-500 text-sm"
    >
      <li
        v-for="(error, i) in errorList"
        :key="i"
      >
        {{ error }}
      </li>
    </ul>
  </div>
</template>
