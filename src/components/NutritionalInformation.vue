<script setup lang="ts">
import type { NutritionInformation } from "@/types/recipes";

import { computed } from "vue";
import { useI18n } from "vue-i18n";

const props = defineProps<{ nutrition: NutritionInformation }>();
const { t } = useI18n();

const snakeToCamel = (value: string) => value.replace(/(_\w)/g, (g: string) => g[1].toUpperCase());
const getUnit = (name: string) => (["potassium", "sodium", "cholesterol"].includes(name) ? "mg" : "g");

const nutrients = computed(
  (): Partial<Omit<NutritionInformation, "calories" | "serving_size">> =>
    Object.fromEntries(
      Object.entries(props.nutrition).filter(
        ([key, value]) => !["calories", "serving_size"].includes(key) && typeof value === "number",
      ),
    ),
);
</script>

<template>
  <Panel
    toggleable
    :collapsed="true"
    itemprop="nutrition"
    itemscope
    itemtype="https://schema.org/NutritionInformation"
  >
    <template #header>
      <h3>{{ t("nutritional_information.title") }}</h3>
    </template>
    <table class="w-full text-left">
      <thead>
        <tr>
          <th
            colspan="2"
            class="text-xs"
          >
            {{ t("nutritional_information.serving_size", nutrition.serving_size) }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class="text-2xl">{{ t("nutritional_information.calories") }}</th>
          <td class="text-2xl text-right font-bold">{{ nutrition.calories }}</td>
        </tr>
        <tr
          v-for="[nutrient, value] in Object.entries(nutrients)"
          :key="nutrient"
          :itemprop="`${snakeToCamel(nutrient)}Content`"
        >
          <th class="capitalize">{{ t(`nutritional_information.${nutrient}`) }}</th>
          <td class="text-right">{{ t(`nutritional_information.value_${getUnit(nutrient)}`, { value }) }}</td>
        </tr>
      </tbody>
    </table>
  </Panel>
</template>
