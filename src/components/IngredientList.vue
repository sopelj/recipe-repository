<script setup lang="ts">
import type { Ingredient, IngredientGroup } from "@/types/recipes";

import { computed } from "vue";
import { useI18n } from "vue-i18n";

const props = defineProps<{ ingredients: Ingredient[]; groups: IngredientGroup[] }>();

const { t } = useI18n();

const groupMapping = computed(() =>
  props.groups.reduce((acc: Record<string, string>, group: IngredientGroup) => {
    acc[group.id.toString()] = group.name;
    return acc;
  }, {}),
);

const groupedIngredients = computed(() =>
  Object.groupBy(props.ingredients, ({ group_id }) =>
    group_id ? groupMapping.value[group_id.toString()] : "",
  ),
);
</script>

<template>
  <div
    v-for="[group, groupIngredients] in Object.entries(groupedIngredients)"
    :key="group"
  >
    <h3
      v-if="group"
      class="pt-4"
    >
      {{ group }}
    </h3>
    <ul>
      <li
        v-for="ingredient in groupIngredients"
        :key="ingredient.id"
        itemprop="recipeIngredient"
      >
        <I18nT
          keypath="recipe.ingredient"
          tag="span"
        >
          <template #amount>{{ ingredient.amount_display }}</template>
          <template #ingredient>
            <strong>{{ ingredient.food_display }}</strong>
          </template>
        </I18nT>
        <span
          v-if="ingredient.qualifier"
          class="qualifier"
        >
          {{ t("recipe.ingredient_qualifier", { qualifier: ingredient.qualifier }) }}
        </span>
        <span
          v-if="ingredient.optional"
          class="optional"
        >
          {{ t("recipe.ingredient_optional") }}
        </span>
        <span v-if="ingredient.note">{{ t("recipe.ingredient_note", { note: ingredient.note }) }}</span>
      </li>
    </ul>
  </div>
</template>
