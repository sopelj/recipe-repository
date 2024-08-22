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
    <InputGroup class="grow-0">
      <Button
        :disabled="form.servings / 2 <= 0.125"
        :loading="form.processing"
        @click="updateServings(0.5)"
      >
        {{ t("recipe.scale_halve") }}
      </Button>
      <InputNumber
        v-model="form.servings"
        placeholder="servings"
        :min="0.125"
        :max="100"
        input-class="text-center pa-0"
        :fluid="true"
        :disabled="form.processing"
        @update:model-value="updateServings(1)"
      />
      <Button
        :disabled="form.servings * 2 >= 50"
        :loading="form.processing"
        @click="updateServings(2)"
      >
        {{ t("recipe.scale_double") }}
      </Button>
    </InputGroup>
    <Message
      v-if="form.errors?.servings"
      severity="error"
    >
      {{ form.errors?.servings }}
    </Message>
  </div>
</template>
