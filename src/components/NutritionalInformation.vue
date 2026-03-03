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
  <div class="border p-2 rounded-md overflow-hidden">
    <button
      type="button"
      class="w-full rounded-md collapse-toggle btn-text flex items-center cursor-pointer"
      data-collapse="#nutrition-info-collapse-content"
    >
      <span class="flex-item grow text-left">{{ t("nutritional_information.title") }}</span>
      <span class="icon-[tabler--chevron-down] collapse-open:rotate-180 size-4"></span>
    </button>
    <div
      id="nutrition-info-collapse-content"
      itemprop="nutrition"
      itemscope
      itemtype="https://schema.org/NutritionInformation"
      class="collapse hidden card w-full overflow-hidden transition-[height] duration-300"
    >
      <table class="w-full text-left card-body">
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
            <td class="text-right">
              {{ t(`nutritional_information.value_${getUnit(nutrient)}`, { value }) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
