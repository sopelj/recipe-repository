<script setup lang="ts" generic="T extends IngredientGroup">
import type { IngredientGroup } from "@/types/recipes";

import { useI18n } from "vue-i18n";

import { useOrderableItems } from "@/composables/orderable-items";

import SortableList from "@/components/SortableList.vue";

const ingredientGroups = defineModel<T[]>({ required: true });

const { t } = useI18n();

const { addItem, deleteItem } = useOrderableItems<IngredientGroup>(ingredientGroups, {
  id: null,
  order: ingredientGroups.value.length + 1,
  name: "",
});
</script>

<template>
  <div class="card p-4">
    <div class="card-title pb-2">
      <div class="flex flex-row items-center">
        <h2 class="text-xxl grow w-100 mr-2">{{ t("edit.ingredientGroups") }}</h2>
      </div>
    </div>
    <div class="card-body">
      <div v-if="!ingredientGroups.length">
        {{ t("edit.no_ingredient_groups") }}
      </div>
      <sortable-list v-model="ingredientGroups">
        <template #default="{ item: group }">
          <div class="flex items-center gap-2">
            <span class="icon-[tabler--grip-vertical] cursor-move"></span>
            <input
              v-model="group.name"
              class="input grow"
            />
            <button
              type="button"
              class="btn-outline cursor-pointer grow-0 shrink-0"
              @click="deleteItem(group)"
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
        {{ t("edit.add_group") }}
      </button>
    </div>
  </div>
</template>
