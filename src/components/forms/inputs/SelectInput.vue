<script setup lang="ts" generic="T extends { id: number | null }">
import { useI18n } from "vue-i18n";

interface Props {
  label?: string;
  id: string;
  options: T[];
  labelKey?: keyof T;
  errors?: string[];
}

const model = defineModel<number | null>();
withDefaults(defineProps<Props>(), {
  label: "",
  labelKey: "label" as keyof T,
  errors: () => [],
});

const { t } = useI18n();
</script>

<template>
  <div class="w-full">
    <label
      v-if="label"
      class="label-text"
      :for="id"
    >
      {{ label }}
    </label>
    <select
      :id="id"
      v-model.number="model"
      class="select"
      :class="errors?.length ? 'is-invalid' : ''"
    >
      <option disabled>
        {{ t("select.options") }}
      </option>
      <option
        v-for="(option, i) in options"
        :key="i"
        :value="option.id"
      >
        <slot
          name="option"
          :option="option"
        >
          {{ option[labelKey as keyof T] }}
        </slot>
      </option>
    </select>
    <ul
      v-if="errors?.length"
      class="text-red-500 text-sm"
    >
      <li v-for="error in errors">{{ error }}</li>
    </ul>
  </div>
</template>
