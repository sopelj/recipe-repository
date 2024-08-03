<script setup lang="ts">
import { Head as IHead } from '@inertiajs/vue3'

defineProps<{ title?: string }>();
</script>

<template>
  <i-head :title="title ? `${title} - Recipe Repository` : 'Recipe Repository'">
    <slot />
  </i-head>
</template>
