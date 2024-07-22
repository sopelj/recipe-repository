<script setup lang="ts">
import { Recipe } from "../types/recipes";

defineProps<{ recipe: Recipe }>();
</script>

<template>
  <div class="container mx-auto">
    <div class="grid grid-cols-12 gap-4">
      <div class="col-span-12 sm:col-span-10 md:col-span-8">
        <h1 class="text-2xl mb-2">{{ recipe.name }}</h1>
        <div class="info">
          <Rating v-model="recipe.avg_rating" :readonly="true" v-tooltip="`${recipe.num_ratings} ratings`"/>
          <div class="mt-2">
            <Tag :value="category.name" severity="secondary" v-for="category in recipe.categories" />
          </div>
          <div v-if="recipe.yield_unit">
            Yields: {{ recipe.yield_amount }} {{ recipe.yield_unit }}
          </div>
          <div v-if="recipe.servings">
            Servings: {{ recipe.servings }}
          </div>
          <div v-if="recipe.source">
            <div v-if="recipe.source.type === 1">
              From: <a :href="recipe.source_value" target="_blank">{{ recipe.source.name }}</a>
            </div>
          </div>
          <Panel v-if="recipe.nutrition" header="Nutritional Information" toggleable>
            {{ recipe.nutrition }}
          </Panel>
          <Divider />
          <div class="mt-2">{{ recipe.description }}</div>
          <Divider />
        </div>
        <div class="ingredients">
          <h2 class="text-xl">Ingredients</h2>
          <Card>
            <template #content>
              {{ recipe.ingredients }}
            </template>
          </Card>
        </div>
      </div>
      <div v-if="recipe.thumbnail_image_url" class="col-span-12 sm:col-span-2 md:col-span-4">
        <img :src="recipe.thumbnail_image_url" alt="" class="w-full border-gray-700 border-2 rounded-md" />
      </div>
      <div class="col-span-12">
        <h2 class="text-xl mb-2">Directions</h2>
        <Panel v-for="step in recipe.steps" :key="step.order" toggleable class="mb-2" :header="`Step ${step.order}`">
          {{ step.text }}
        </Panel>
      </div>
    </div>
  </div>
</template>
