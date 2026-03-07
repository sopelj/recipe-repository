<script setup lang="ts">
const model = defineModel<number | null>({ default: 0 });
const props = withDefaults(
  defineProps<{
    title?: string;
    disabled?: boolean;
    readonly?: boolean;
    size?: number;
  }>(),
  { size: 6, disabled: false, readonly: false, title: undefined },
);

const setRating = (val: number) => {
  if (props.disabled || props.readonly) return;
  model.value = model.value === val ? 0 : val;
};
</script>

<template>
  <div
    class="flex justify-center"
    :title="title"
    :aria-label="title"
  >
    <button
      v-for="star in 5"
      :key="star"
      type="button"
      :disabled="disabled"
      class="focus:outline-none"
      :class="[
        disabled || readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110 transition-transform',
      ]"
      @click="setRating(star)"
    >
      <span
        :class="[
          `size-${size}`,
          (model ?? 0) >= star
            ? 'icon-[tabler--star-filled] text-yellow-400'
            : 'icon-[tabler--star] text-gray-300',
        ]"
      ></span>
    </button>
  </div>
</template>
