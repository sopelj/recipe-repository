<script setup lang="ts">
withDefaults(defineProps<{ src: string; alt?: string }>(), { alt: "" });
</script>

<template>
  <div class="h-full w-full aspect-square">
    <img
      v-if="src"
      :src="src"
      :alt="alt"
      loading="lazy"
      class="h-full w-full object-cover"
    />
    <div
      v-else
      class="w-full h-full bg-slate-100 text-slate-400 dark:bg-gray-700 dark:text-gray-500 flex justify-center items-center"
    >
      <i class="pi pi-image text-2xl" />
    </div>
  </div>
</template>
