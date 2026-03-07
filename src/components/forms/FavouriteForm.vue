<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useToast } from "vue-toastification";

const props = defineProps<{ userFavourite: boolean }>();

const { t } = useI18n();
const toast = useToast();
const form = useForm({ favourite: props.userFavourite });

const setFavourite = (state: boolean) => {
  form.favourite = state;
  form.post(`${window.location.pathname}${window.location.search}`, {
    only: ["userFavourite"],
    preserveScroll: true,
    viewTransition: false,
  });
};

onMounted(() => {
  if (form.errors?.favourite) {
    toast.error(form.errors.favourite);
    form.clearErrors("favourite");
  }
});
</script>

<template>
  <button
    :title="userFavourite ? t('recipe.un-favourite') : t('recipe.favourite')"
    :disabled="form.processing"
    class="btn-text text-3xl hover:text-purple-400 transition-colors cursor-pointer"
    @click="setFavourite(!userFavourite)"
  >
    <span
      v-if="userFavourite"
      class="icon-[mdi--heart]"
    ></span>
    <span
      v-else
      class="icon-[mdi--heart-outline]"
    ></span>
  </button>
</template>
