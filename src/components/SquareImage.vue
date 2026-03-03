<script setup lang="ts">
withDefaults(defineProps<{ src: string | null; alt?: string; style?: string }>(), { alt: "", style: "" });
</script>

<template>
  <div class="h-full w-full aspect-square">
    <img
      v-if="src"
      :src="src"
      :alt="alt"
      :style="style"
      loading="lazy"
      class="h-full w-full object-cover"
    />
    <div
      v-else
      class="w-full h-full bg-slate-100 text-slate-400 dark:bg-gray-700 dark:text-gray-500 flex justify-center items-center"
      :style="style"
    >
      <i class="icon-[mdi-light--image] text-2xl" />
    </div>
  </div>
</template>
