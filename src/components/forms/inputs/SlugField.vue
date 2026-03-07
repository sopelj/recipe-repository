<script setup lang="ts">
import { computed, watch } from "vue";

const model = defineModel<string>();

const props = withDefaults(
  defineProps<{
    id: string;
    sourceValue: string;
    label?: string;
    errors?: string[] | string;
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
watch(
  () => props.sourceValue,
  () => {
    model.value = props.sourceValue.replaceAll(" ", "-").toLocaleLowerCase();
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
      type="text"
      readonly
      tabindex="-1"
      class="input"
      :class="inputClass + (errorList?.length ? ' is-invalid' : '')"
    />
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
