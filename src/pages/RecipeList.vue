<script setup lang="ts">
import type { RecipeItem } from "../types/recipes";
import type { Category } from "../types/categories.ts";

import { computed, ref } from "vue";
import { Link as ILink } from "@inertiajs/vue3"

const props = defineProps<{ recipes: RecipeItem[], "category"?: Category, "parentCategories"?: Category[] }>();
const search = ref<string>("");
const filteredRecipes = computed((): RecipeItem[] => (
    search.value ? props.recipes.filter((r) => !r.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase())) : props.recipes)
);
const title = computed((): string => props.category?.name_plural || props.category?.name || "All recipes");
</script>

<template>
  <div class="container mx-auto">
    <h1 class="text-3xl py-2">{{ title }}</h1>
    <data-view layout="grid" :value="filteredRecipes" data-key="slug">
      <template #header>
        <div class="flex justify-end">
          <icon-field>
            <input-icon class="pi pi-search" />
            <input-text v-model="search" placeholder="Search" />
          </icon-field>
        </div>
      </template>
      <template #grid="{ items }">
        <div class="grid grid-cols-12 gap-4 p-4">
          <i-link
              v-for="recipe in items"
              :key="recipe.slug"
              :href="`/recipes/${recipe.slug}/`"
              class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <Card class="text-center rounded-md overflow-clip border-solid border-2 dark:border-gray-700 w-100">
              <template #title>{{ recipe.name }}</template>
              <template #header>
                <img :src="recipe.thumbnail_image_url" alt="" class="object-cover object-center w-full" />
              </template>
              <template #subtitle>
                <div class="flex items-center flex-col">
                  <Rating v-model="recipe.avg_rating" v-tooltip="`${recipe.num_ratings} ratings`" :readonly="true"/>
                  <div class="mt-2">
                    <Tag v-for="c in recipe.categories" :key="c.slug" :value="c.name" severity="secondary" />
                  </div>
                </div>
              </template>
            </Card>
          </i-link>
        </div>
      </template>
    </data-view>
  </div>
</template>
