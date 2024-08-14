<script setup lang="ts">
defineProps<{ label: string }>();
</script>

<template>
  <div class="flex align-items-center py-3">
    <div class="w-1/4 text-500 font-medium">{{ label }}</div>
    <div class="w-3/4">
      <slot />
    </div>
  </div>
</template>
