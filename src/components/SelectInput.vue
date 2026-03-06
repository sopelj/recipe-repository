<script setup lang="ts" generic="T extends { id: number | null }">
interface Props {
  label?: string;
  id: string;
  options: T[];
  labelKey?: keyof T;
}

const model = defineModel<number | null>();

withDefaults(defineProps<Props>(), {
  label: "",
  labelKey: "label" as keyof T,
});
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
    >
      <option disabled>
        {{ $t("select.options") }}
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
  </div>
</template>
