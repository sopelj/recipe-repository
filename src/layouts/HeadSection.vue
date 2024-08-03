<script setup lang="ts">
import { Head as IHead } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

defineProps<{ title?: string }>();

const { t } = useI18n();
</script>

<template>
  <IHead :title="title ? `${title} - ${t('global.title')}` : t('global.title')">
    <slot />
  </IHead>
</template>
