<script setup lang="ts" generic="T">
const model = defineModel<T>();

withDefaults(
  defineProps<{
    id: string;
    label?: string;
    placeholder?: string;
    errors?: string[];
    inputClass?: string;
  }>(),
  {
    inputClass: "",
    errors: () => [],
  },
);
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
    <textarea
      :id="id"
      v-model="model"
      :placeholder="placeholder"
      class="textarea"
      :class="inputClass + (errors?.length ? ' is-invalid' : '')"
    />
    <ul
      v-if="errors"
      class="text-red-500 text-sm"
    >
      <li v-for="error in errors">{{ error }}</li>
    </ul>
  </div>
</template>
