<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useToast } from "vue-toastification";

import Rating from "@/components/RatingInput.vue";

const props = defineProps<{ numRatings: number; userRating: number | null; averageRating: number | null }>();

const { t } = useI18n();
const toast = useToast();

const form = useForm({ rating: props.userRating || props.averageRating || undefined });

const changeRating = () => {
  form.post(`${window.location.pathname}${window.location.search}`, {
    only: ["userRating", "recipe"],
    preserveScroll: true,
    viewTransition: false,
  });
};

onMounted(() => {
  if (form.errors?.rating) {
    toast.error(form.errors.rating);
    form.clearErrors("rating");
  }
});
</script>

<template>
  <rating
    v-model="form.rating"
    :title="t('recipe.ratings', numRatings)"
    :class="!!userRating ? 'user-rating' : ''"
    :disabled="form.processing"
    @update:model-value="changeRating"
  />
</template>
