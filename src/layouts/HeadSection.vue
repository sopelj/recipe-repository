<script setup lang="ts">
import { Head as IHead } from '@inertiajs/vue3'
import { useI18n } from "vue-i18n";

const { t } = useI18n();

defineProps<{ title?: string }>();
</script>

<template>
  <i-head :title="title ? `${title} - ${t('global.title')}` : t('global.title')">
    <slot />
  </i-head>
</template>
