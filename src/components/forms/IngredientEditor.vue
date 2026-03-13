<script setup lang="ts" generic="T extends EditableIngredient[]">
import type { EditableIngredient, Food, Qualifier, Unit } from "@/types/recipes";

import { Deferred } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import { useOrderableItems } from "@/composables/orderable-items";

import InputField from "@/components/forms/inputs/InputField.vue";
import SelectInput from "@/components/forms/inputs/SelectInput.vue";
import SortableList from "@/components/SortableList.vue";

const ingredients = defineModel<T>({ required: true });
defineProps<{
  errors: Record<string, string | string[]>;
  qualifiers?: Qualifier[];
  foods?: Food[];
  units?: Unit[];
}>();
const { addItem, deleteItem } = useOrderableItems<EditableIngredient>(ingredients, {
  id: null,
  order: 0,
  amount: null,
  amount_max: null,
  food: null,
  unit: null,
  group: null,
  qualifier: null,
  optional: false,
  note: "",
});

const { t } = useI18n();
</script>

<template>
  <sortable-list
    v-model="ingredients"
    row-class="grid grid-flow-col grid-cols-16 gap-2"
  >
    <template #header>
      <div class="">{{ t("edit.order") }}</div>
      <div class="col-span-2">{{ t("edit.amount") }}</div>
      <div class="col-span-3">{{ t("edit.unit") }}</div>
      <div class="col-span-3">{{ t("edit.qualifier") }}</div>
      <div class="col-span-3">{{ t("edit.food") }}</div>
      <div class="text-center">{{ t("edit.optional") }}</div>
      <div class="col-span-3">{{ t("edit.notes") }}</div>
      <div class="col-span-3">{{ t("edit.delete") }}</div>
    </template>
    <template #default="{ item: ingredient, index: i }">
      <div class="flex justify-center cursor-move userselect-none grow-0 shrink-0">
        <span class="icon-[tabler--grip-vertical] text-2xl"></span>
      </div>
      <div class="join col-span-2">
        <input-field
          :id="`ingredient-${i}-amount`"
          v-model="ingredient.amount"
          :errors="errors?.[`ingredients?.[${i}].amount`]"
          class="join-item"
        />
        <input-field
          :id="`ingredient-${i}-amount`"
          v-model="ingredient.amount_max"
          :errors="errors?.[`ingredients?.[${i}].amount_max`]"
          class="join-item"
        />
      </div>
      <deferred data="units">
        <template #fallback>
          <div>Loading...</div>
        </template>
        <select-input
          v-if="units"
          :id="`ingredient-${i}-unit`"
          v-model="ingredient.unit"
          :errors="errors?.[`ingredients?.[${i}].unit`]"
          :options="units"
          label-key="name"
          class="col-span-3"
        >
          <template #option="{ option }">
            {{ option.name }}
            <template v-if="option.abbreviation"> ({{ option.abbreviation }})</template>
          </template>
        </select-input>
      </deferred>
      <deferred data="qualifiers">
        <template #fallback>
          <div>Loading...</div>
        </template>
        <select-input
          v-if="qualifiers"
          :id="`ingredient-${i}-qualifier`"
          v-model="ingredient.qualifier"
          :errors="errors?.[`ingredients?.[${i}].qualifier`]"
          :options="qualifiers"
          label-key="title"
          class="col-span-3"
        />
      </deferred>
      <deferred data="foods">
        <template #fallback>
          <div>Loading...</div>
        </template>
        <select-input
          v-if="foods"
          :id="`ingredient-${i}-food`"
          v-model="ingredient.food"
          :errors="errors?.[`ingredients?.[${i}].food`]"
          :options="foods"
          label-key="name"
          class="col-span-2"
        />
      </deferred>
      <div class="flex justify-center">
        <input
          :id="`optional-${i}`"
          v-model="ingredient.optional"
          type="checkbox"
          class="checkbox grow-0 shrink-0"
        />
        <label
          class="sr-only"
          :for="`optional-${i}`"
        >
          {{ t("edit.optional") }}
        </label>
      </div>
      <input-field
        :id="`ingredient-${i}-note`"
        v-model="ingredient.note"
        :errors="errors?.[`ingredients?.[${i}].note`]"
        class="col-span-3"
      />
      <div class="flex justify-center">
        <button
          type="button"
          class="btn-outline cursor-pointer grow-0 shrink-0"
          @click="deleteItem(ingredient)"
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
    {{ t("edit.add_ingredient") }}
  </button>
</template>
