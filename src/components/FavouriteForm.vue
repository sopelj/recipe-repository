<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onMounted } from "vue";

import { useToast } from "primevue/usetoast";

const props = defineProps<{ userFavourite: boolean }>();

const toast = useToast();

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
    :icon="userFavourite ? 'pi pi-heart-fill' : 'pi pi-heart'"
    :disabled="form.processing"
    text
    @click="setFavourite(!userFavourite)"
  />
</template>
