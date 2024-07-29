<script setup lang="ts">
import type { NutritionInformation } from "../types/recipes";
import { computed } from "vue";

const props = defineProps<{ nutrition: NutritionInformation }>()

const snakeToCamel = (value: string) => value.replace(/(_\w)/g, (g: string) => g[1].toUpperCase());
const getUnit = (name: string): string => {
  if (["calories", "servingSize"].includes(name)) {
    return ""
  }
  if (["potassiumContent", "sodiumContent", "cholesterolContent"].includes(name)) {
    return "mg";
  }
  return "g";
};

const nutritionalInformation = computed((): Record<string, number> | undefined => (
    props.nutrition ? Object.entries(props.nutrition).reduce((acc, [key, value]) => {
      if (typeof value === "number") {
        const name = ["calories", "serving_size"].includes(key) ? key : `${key}_content`;
        acc[snakeToCamel(name)] = value;
      }
      return acc;
    }, {} as Record<string, number>) : undefined
));
</script>

<template>
  <Panel
      v-if="nutritionalInformation"
      header="Nutritional Information"
      toggleable
      :collapsed="true"
      itemprop="nutrition"
      itemscope
      itemtype="https://schema.org/NutritionInformation"
  >
    <div v-for="[key, value] in Object.entries(nutritionalInformation)" :itemprop="key" :key="key">
      {{ key }}: {{ value }}{{ getUnit(key) }}
    </div>
  </Panel>
</template>
