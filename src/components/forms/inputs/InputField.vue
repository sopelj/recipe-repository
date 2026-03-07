<script setup lang="ts" generic="T">
const model = defineModel<T>();

withDefaults(
  defineProps<{
    id: string;
    label?: string;
    placeholder?: string;
    errors?: string[];
    type?: string;
    inputClass?: string;
  }>(),
  {
    inputClass: "",
    type: "text",
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
    <input
      :id="id"
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      class="input"
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
