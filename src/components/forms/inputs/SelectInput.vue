<script setup lang="ts" generic="T extends { id: number | null }">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

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
      v-if="errorList"
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
