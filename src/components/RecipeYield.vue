<script setup lang="ts">
import type { YieldUnit } from "@/types/recipes";

import { computed } from "vue";
import { useI18n } from "vue-i18n";

const props = defineProps<{ amount: number; baseServings: number; servings: number; unit: YieldUnit }>();

const { t, rt } = useI18n();

const yieldAmount = computed(() => props.amount * (props.servings / props.baseServings));
const yieldLabel = computed(() => {
  return rt(`${props.unit.name} | ${props.unit.name_plural || props.unit.name}`, yieldAmount.value);
});
</script>

<template>
  <span itemprop="recipeYield">
    {{ yieldAmount }} {{ yieldLabel }} ({{ t("recipe.servings", servings) }})
  </span>
</template>
