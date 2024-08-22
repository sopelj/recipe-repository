<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";

import { useToast } from "primevue/usetoast";

const props = defineProps<{ userFavourite: boolean }>();

const toast = useToast();

const { t } = useI18n();
const form = useForm({ favourite: props.userFavourite });

const setFavourite = (state: boolean) => {
  form.favourite = state;
  form.post(`${window.location.pathname}${window.location.search}`, {
    only: ["userFavourite"],
    preserveScroll: true,
  });
};

onMounted(() => {
  if (form.errors?.favourite) {
    toast.add({ severity: "error", detail: form.errors.favourite });
    form.clearErrors("favourite");
  }
});
</script>

<template>
  <Button
    v-tooltip="userFavourite ? t('recipe.un-favourite') : t('recipe.favourite')"
    :icon="userFavourite ? 'pi pi-heart-fill' : 'pi pi-heart'"
    :disabled="form.processing"
    text
    @click="setFavourite(!userFavourite)"
  />
</template>
