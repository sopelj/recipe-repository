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
      class="w-full h-full bg-slate-100 flex justify-center items-center"
    >
      <i class="pi pi-image text-2xl" />
    </div>
  </div>
</template>
