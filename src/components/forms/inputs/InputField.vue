<script setup lang="ts" generic="T">
import { computed } from "vue";

const model = defineModel<T>();

const props = withDefaults(
  defineProps<{
    id: string;
    label?: string;
    placeholder?: string;
    errors?: string[] | string;
    type?: string;
    inputClass?: string;
  }>(),
  {
    label: undefined,
    placeholder: undefined,
    inputClass: "",
    type: "text",
    errors: () => [],
  },
);

const errorList = computed((): string[] => (Array.isArray(props.errors) ? props.errors : [props.errors]));
</script>

<template>
  <div class="w-full input">
    <label
      v-if="label"
      class="label-text"
      :for="id"
    >
      {{ label }}
    </label>
    <input
      :id="id"
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      :class="inputClass + (errorList?.length ? ' is-invalid' : '')"
    />
    <ul
      v-if="errorList?.length"
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
