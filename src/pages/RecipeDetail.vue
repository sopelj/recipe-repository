<script setup lang="ts">
import type { Recipe, Ingredient } from "../types/recipes";
import PButton from "primevue/button";
import NutritionalInformation from "../components/NutritionalInformation.vue";
import {ref} from "vue";

const props = defineProps<{ recipe: Recipe, ingredients: Ingredient[] }>();

const formatDuration = (duration: string) => {
  const [h, m, s] = duration.split(":");
  return Object.entries({h, m, s}).reduce((acc, [n, v]) => {
    const f = parseInt(v);
    return f ? acc + ` ${f}${n}` : acc;
  }, "").trim();
}

const formatIsoDuration = (duration: string): string => `PT${formatDuration(duration).replace(" ", "").toUpperCase()}`;
const servings = ref<number>(props.recipe.servings || 1);
</script>

<template>
  <div class="container mx-auto" itemscope itemtype="https://schema.org/Recipe">
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 sm:col-span-10 md:col-span-8">
        <div class="flex">
          <h1 class="text-4xl mb-4 cursive flex-grow" itemprop="name">{{ recipe.name }}</h1>
          <rating
            v-tooltip="`${recipe.num_ratings} ratings`"
            :model-value="recipe.avg_rating"
            :readonly="true"
          />
        </div>
        <div v-if="recipe.categories" class="flex align-items-center py-3">
          <div class="w-1/4 text-500 font-medium">Categories:</div>
          <div class="w-3/4">
            <tag v-for="c in recipe.categories" :key="c.slug" :value="c.name" severity="secondary" />
          </div>
        </div>
        <div class="flex align-items-center py-3">
          <div class="w-1/4 text-500 font-medium">Yields:</div>
          <div class="w-3/4">
            <span v-if="recipe.yield_unit" itemprop="recipeYield">{{ recipe.yield_amount }} {{ recipe.yield_unit }} ({{ servings }} servings)</span>
            <span v-else>{{ servings }} servings</span>
          </div>
        </div>
        <div v-if="recipe.source" class="flex align-items-center py-3">
          <div class="w-1/4 text-500 font-medium">From:</div>
          <div class="w-3/4" itemprop="isBasedOn" itemscope itemtype="https://schema.org/CreativeWork">
            <div v-if="recipe.source.type === 1">
              <link itemprop="url" :href="recipe.source_value"/>
              <a :href="recipe.source_value" itemprop="publisher" target="_blank" class="underline">{{ recipe.source.name }}</a>
            </div>
          </div>
        </div>
        <divider v-if="recipe.description" />
        <div class="my-2" itemprop="description">{{ recipe.description }}</div>
        <splitter v-if="recipe.total_time" class="mb-5">
            <splitter-panel v-if="recipe.prep_time" class="flex items-center justify-center">
              Prep time: <meta itemprop="prepTime" :content="formatIsoDuration(recipe.prep_time)">{{ formatDuration(recipe.prep_time) }}
            </splitter-panel>
            <splitter-panel v-if="recipe.cook_time" class="flex items-center justify-center">
              Cook time: <meta itemprop="prepTime" :content="formatIsoDuration(recipe.cook_time)">{{ formatDuration(recipe.cook_time) }}
            </splitter-panel>
            <splitter-panel v-if="recipe.total_time" class="flex items-center justify-center">
              Total time: <meta itemprop="prepTime" :content="formatIsoDuration(recipe.total_time)">{{ formatDuration(recipe.total_time) }}
            </splitter-panel>
        </splitter>
        <div class="ingredients">
          <card>
            <template #title>
              <div class="flex flex-row items-center">
                <h2 class="text-xl grow w-100">Ingredients</h2>
                <div class="grow-0">
                  <input-group class="grow-0">
                    <p-button :disabled="servings <= 0.125" @click="servings /= 2">½</p-button>
                    <input-number v-model="servings" placeholder="servings" :min="0.125" :max="100" input-class="text-center pa-0" :fluid="true"/>
                    <p-button :disabled="servings >= 100" @click="servings *= 2">x2</p-button>
                  </input-group>
                </div>
              </div>
            </template>
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
          </card>
        </div>
      </div>
      <div class="col-span-12 sm:col-span-2 md:col-span-4">
        <div v-if="recipe.thumbnail_image_url" class="overflow-clip p-card">
            <img :src="recipe.thumbnail_image_url" :alt="recipe.name" class="w-full" />
        </div>
        <nutritional-information v-if="recipe.nutrition" :nutrition="recipe.nutrition" :servings="servings" class="mt-4" />
      </div>
      <div class="col-span-8">
        <h2 class="text-xl mb-2">Directions</h2>
        <Panel v-for="(step, i) in recipe.steps" :key="i" toggleable class="mb-2" :header="`Step ${i + 1}`" itemprop="recipeInstructions">
          {{ step }}
        </Panel>
      </div>
    </div>
  </div>
</template>