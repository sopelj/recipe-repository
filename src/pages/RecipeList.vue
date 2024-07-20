<script setup lang="ts">
import Card from "primevue/card";
import Image from "primevue/image";
import Rating from "primevue/rating";
import { Link } from "@inertiajs/vue3"
import type { RecipeItem } from "../types/recipes";

defineProps<{ recipes: RecipeItem[] }>();
</script>

<template>
  <div class="container mx-auto">
    <h1>Recipes</h1>
    <div class="grid gap-4 grid-flow-col auto-cols-[minmax(0,_2fr)]">
      <Card v-for="recipe in recipes" class="text-center w-100">
        <template #title>{{ recipe.name }}</template>
        <template #header>
          <Image :src="recipe.thumbnail_url" alt="" />
        </template>
        <template #subtitle>
          <Rating v-model="recipe.avg_rating" :readonly="true" /> ({{ recipe.num_ratings }} ratings)
          <Link :href="`/recipes/${recipe.slug}/`">View</Link>
        </template>
      </Card>
    </div>
  </div>
</template>
