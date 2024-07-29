<script setup lang="ts">
import type { Recipe, Ingredient } from "../types/recipes";
import PButton from "primevue/button";
import NutritionalInformation from "../components/NutritionalInformation.vue";

defineProps<{ recipe: Recipe, ingredients: Ingredient[] }>();

const formatDuration = (duration: string) => {
  const [h, m, s] = duration.split(":");
  return Object.entries({h, m, s}).reduce((acc, [n, v]) => {
    const f = parseInt(v);
    return f ? acc + ` ${f}${n}` : acc;
  }, "").trim();
}

const formatIsoDuration = (duration: string): string => `PT${formatDuration(duration).replace(" ", "").toUpperCase()}`;
</script>

<template>
  <div class="container mx-auto" itemscope itemtype="https://schema.org/Recipe">
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 sm:col-span-10 md:col-span-8">
        <h1 class="text-2xl mb-2" itemprop="name">{{ recipe.name }}</h1>
        <div class="info">
          <Rating
              v-tooltip="`${recipe.num_ratings} ratings`"
              :model-value="recipe.avg_rating"
              :readonly="true"
          />
          <div class="mt-2">
            <Tag v-for="c in recipe.categories" :key="c.slug" :value="c.name" severity="secondary" />
          </div>
          <div v-if="recipe.yield_unit">
            Yields: <span itemprop="recipeYield">{{ recipe.yield_amount }} {{ recipe.yield_unit }}</span>
          </div>
          <div v-if="recipe.servings">
            Servings: {{ recipe.servings }}
          </div>
          <div v-if="recipe.prep_time">
            Prep time: <meta itemprop="prepTime" :content="formatIsoDuration(recipe.prep_time)">{{ formatDuration(recipe.prep_time) }}
          </div>
          <div v-if="recipe.cook_time">
            Cook time: <meta itemprop="cookTime" :content="formatIsoDuration(recipe.cook_time)">{{ formatDuration(recipe.cook_time) }}
          </div>
          <div v-if="recipe.total_time">
            Total time: <meta itemprop="totalTime" :content="formatIsoDuration(recipe.total_time)">{{ formatDuration(recipe.total_time) }}
          </div>
          <div v-if="recipe.source" itemprop="isBasedOn" itemscope itemtype="https://schema.org/CreativeWork">
            <div v-if="recipe.source.type === 1">
              <link itemprop="url" :href="recipe.source_value"/>
              From: <a :href="recipe.source_value" itemprop="publisher" target="_blank">{{ recipe.source.name }}</a>
            </div>
          </div>
          <nutritional-information v-if="recipe.nutrition" :nutrition="recipe.nutrition" />
          <Divider />
          <div class="mt-2" itemprop="description">{{ recipe.description }}</div>
          <Divider />
        </div>
        <div class="ingredients">
          <div class="flex flex-row items-center">
            <h2 class="text-xl grow w-100">Ingredients</h2>
            <div class="grow-0">
              <input-group class="grow-0">
                <p-button icon="pi pi-plus" :disabled="!!recipe.servings" />
                <input-number placeholder="Price" :model-value="recipe.servings" :min="0" input-class="w-[3rem]" :fluid="true"/>
                <p-button icon="pi pi-minus" :disabled="!!recipe.servings" />
              </input-group>
            </div>
          </div>
          <Card>
            <template #content>
              <ul>
                <li v-for="ingredient in ingredients" :key="ingredient.id">
                  <span>{{ ingredient.amount_display }}<strong>&nbsp;{{ ingredient.food_display }}</strong></span>
                  <span v-if="ingredient.qualifier" class="qualifier">, {{ ingredient.qualifier }}</span>
                  <span v-if="ingredient.optional" class="optional">*Optional</span>
                  <span v-if="ingredient.note">&nbsp;({{ ingredient.note }})</span>
                </li>
              </ul>
            </template>
          </Card>
        </div>
      </div>
      <div v-if="recipe.thumbnail_image_url" class="col-span-12 sm:col-span-2 md:col-span-4">
        <img :src="recipe.thumbnail_image_url" alt="" class="w-full border-gray-700 border-2 rounded-md" />
      </div>
      <div class="col-span-12">
        <h2 class="text-xl mb-2">Directions</h2>
        <Panel v-for="(step, i) in recipe.steps" :key="i" toggleable class="mb-2" :header="`Step ${i + 1}`" itemprop="recipeInstructions">
          {{ step }}
        </Panel>
      </div>
    </div>
  </div>
</template>
