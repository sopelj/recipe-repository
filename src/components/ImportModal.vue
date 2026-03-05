<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { onBeforeUnmount, onMounted } from "vue";
import { useI18n } from "vue-i18n";

const isOpen = defineModel<boolean>();

const { t } = useI18n();

const importForm = useForm({
  url: "",
});

const importRecipe = () => {
  importForm.post(t("routes.recipe_import"), { preserveScroll: true });
};

const closeModal = () => {
  importForm.resetAndClearErrors();
  isOpen.value = false;
};

const onPressCloseModal = (e: KeyboardEvent) => {
  if (e.key === "Escape") {
    closeModal();
  }
};

onMounted(() => {
  document.addEventListener("keydown", onPressCloseModal);
});
onBeforeUnmount(() => {
  document.removeEventListener("keydown", onPressCloseModal);
});
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed top-0 left-0 w-full h-full bg-base-300/60 z-50"
    role="dialog"
    tabindex="-1"
    :class="isOpen ? 'open opened' : 'hidden'"
  >
    <div
      class="modal-dialog fixed grid h-screen place-items-center"
      @click.self="closeModal"
    >
      <div class="modal-content">
        <div class="modal-header pb-0">
          <h3 class="modal-title">{{ t("recipe.import") }}</h3>
          <button
            type="button"
            class="btn btn-text btn-circle btn-sm top-3"
            aria-label="Close"
            @click="closeModal"
          >
            <span class="icon-[tabler--x] size-4"></span>
          </button>
        </div>
        <form @submit.prevent="importRecipe">
          <div class="modal-body">
            <div class="form-control">
              <label
                class="label"
                for="import-url"
              >
                <span class="label-text">URL</span>
              </label>
              <input
                id="import-url"
                v-model="importForm.url"
                type="url"
                class="input input-bordered w-full"
                placeholder="https://example.com/"
                required
              />
              <label
                v-if="importForm.errors.url"
                class="label"
              >
                <span class="label-text-alt text-error">{{ importForm.errors.url }}</span>
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="importForm.processing"
            >
              <span
                v-if="importForm.processing"
                class="loading loading-spinner"
              ></span>
              {{ t("recipe.import") }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
