<script setup lang="ts">
import { Head } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

defineProps<{ title?: string }>();

const { t } = useI18n();
</script>

<template>
  <Head :title="title ? `${title} - ${t('global.title')}` : t('global.title')">
    <slot />
  </Head>
</template>
