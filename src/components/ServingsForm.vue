<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

const props = defineProps<{ servings: number }>();

const { t } = useI18n();
const form = useForm({ servings: props.servings });

const updateServings = (multiplier: number) => {
  if (!form.servings) {
    form.servings = props.servings;
    return;
  }
  const newValue = form.servings * multiplier;
  if (newValue > 50 || newValue < 0.125) {
    form.setError("servings", t("recipe.scale_outside_range"));
    form.servings = props.servings;
    return;
  }
  form.servings = newValue;
  form.get(window.location.pathname, { only: ["ingredients", "servings"], preserveScroll: true });
};
</script>

<template>
  <div class="grow-0 ml-4">
    <div class="grow-0 join">
      <button
        :disabled="form.servings / 2 <= 0.125 || form.processing"
        class="btn join-item"
        type="button"
        @click="updateServings(0.5)"
      >
        {{ t("recipe.scale_halve") }}
        <span
          v-if="form.processing"
          class="icon-[codex--loader]"
        ></span>
      </button>
      <input
        v-model="form.servings"
        placeholder="servings"
        :min="0.125"
        :max="100"
        class="text-center pa-0 join-item"
        :disabled="form.processing"
        @update:model-value="updateServings(1)"
      />
      <button
        :disabled="form.servings * 2 >= 50 || form.processing"
        class="btn join-item"
        type="button"
        @click="updateServings(2)"
      >
        {{ t("recipe.scale_double") }}
        <span
          v-if="form.processing"
          class="icon-[codex--loader]"
        ></span>
      </button>
    </div>
    <div
      v-if="form.errors?.servings"
      class="text-red-500"
    >
      {{ form.errors?.servings }}
    </div>
  </div>
</template>
