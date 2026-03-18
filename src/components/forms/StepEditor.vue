<script setup lang="ts" generic="T extends Step">
import type { Step } from "@/types/recipes";

import { useI18n } from "vue-i18n";

import { useOrderableItems } from "@/composables/orderable-items";

import TextInput from "@/components/forms/inputs/TextInput.vue";
import SortableList from "@/components/SortableList.vue";

const steps = defineModel<T[]>("steps", { required: true });
defineProps<{ errors: Record<string, string | string[]> }>();
const { addItem, deleteItem } = useOrderableItems<Step>(steps, {
  id: null,
  order: steps.value.length + 1,
  text: "",
});

const { t } = useI18n();
</script>

<template>
  <div class="steps">
    <div v-if="!steps?.length">
      {{ t(" edit.no_steps") }}
    </div>
    <sortable-list v-model="steps">
      <template #default="{ item: step, index: i }">
        <div class="card mb-2 flex flex-row items-center cursor-move">
          <span class="ml-4 icon-[tabler--grip-vertical]"></span>
          <h3 class="card-title py-4 pr-4">{{ t("recipe.step_title", { step: step.order }) }}</h3>
          <div class="card-body py-4 grow">
            <text-input
              :id="`step-${step.order}-text`"
              v-model="step.text"
              :errors="errors?.[`steps?.[${i}].text`]"
            />
          </div>
          <button
            type="button"
            class="btn-outline cursor-pointer mr-4 px-2"
            @click="deleteItem(step)"
          >
            <span class="icon-[ic--outline-delete-outline] text-3xl"></span>
          </button>
        </div>
      </template>
    </sortable-list>
    <button
      type="button"
      class="btn btn-secondary mt-4"
      @click="addItem"
    >
      {{ t("edit.add_step") }}
    </button>
  </div>
</template>
