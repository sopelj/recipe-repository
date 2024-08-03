<script setup lang="ts">
import type { NutritionInformation } from "../types/recipes";
import { computed } from "vue";

const props = defineProps<{ nutrition: NutritionInformation }>();

const snakeToCamel = (value: string) => value.replace(/(_\w)/g, (g: string) => g[1].toUpperCase());
const getUnit = (name: string): string =>
  ["potassiumContent", "sodiumContent", "cholesterolContent"].includes(name) ? "mg" : "g";

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
    header="Nutritional Information"
    toggleable
    :collapsed="true"
    itemprop="nutrition"
    itemscope
    itemtype="https://schema.org/NutritionInformation"
  >
    <table class="w-full text-left">
      <thead>
        <tr>
          <th
            colspan="2"
            class="text-xs"
          >
            Amount per {{ nutrition.serving_size }} serving
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class="text-2xl">Calories</th>
          <td class="text-2xl text-right font-bold">{{ nutrition.calories }}</td>
        </tr>
        <tr
          v-for="[nutrient, value] in Object.entries(nutrients)"
          :key="nutrient"
          :itemprop="`${snakeToCamel(nutrient)}Content`"
        >
          <th class="capitalize">{{ nutrient.replace("_", " ") }}</th>
          <td class="text-right">{{ value }}{{ getUnit(nutrient) }}</td>
        </tr>
      </tbody>
    </table>
  </Panel>
</template>
