<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";

import { useToast } from "primevue/usetoast";

const props = defineProps<{ numRatings: number; userRating: number | null; averageRating: number | null }>();

const toast = useToast();

const { t } = useI18n();

const form = useForm({ rating: props.userRating || props.averageRating || undefined });

const changeRating = () => {
  form.post(`${window.location.pathname}${window.location.search}`, {
    only: ["userRating", "recipe"],
    preserveScroll: true,
  });
};

onMounted(() => {
  if (form.errors?.rating) {
    toast.add({ severity: "error", detail: form.errors.rating });
    form.clearErrors("rating");
  }
});
</script>

<template>
  <Rating
    v-model="form.rating"
    v-tooltip="t('recipe.ratings', numRatings)"
    :class="!!userRating ? 'user-rating' : ''"
    :disabled="form.processing"
    @update:model-value="changeRating"
  />
</template>

<style scoped>
.user-rating :deep(.p-rating-on-icon) {
  color: var(--p-primary-600) !important;
}
</style>
