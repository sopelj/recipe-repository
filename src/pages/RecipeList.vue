<script setup lang="ts">
import type { RecipeItem } from "../types/recipes";
import { computed, ref } from "vue";
import { Link } from "@inertiajs/vue3"

const props = defineProps<{ recipes: RecipeItem[] }>();
const search = ref<string>("");
const filteredRecipes = computed((): RecipeItem[] => (
    search.value ? props.recipes.filter((r) => !r.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase())) : props.recipes)
);
</script>

<template>
  <div class="container mx-auto">
    <h1 class="sr-only">Recipes</h1>
    <DataView layout="grid" :value="filteredRecipes">
      <template #header>
        <div class="flex justify-end">
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="search" placeholder="Search" />
          </IconField>
        </div>
      </template>
      <template #grid="{ items }">
        <div class="grid grid-cols-12 gap-4">
          <Link
              :href="`/recipes/${recipe.slug}/`"
              v-for="recipe in items"
              :key="recipe.slug"
              class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <Card class="text-center rounded-md overflow-clip border-solid border-2 dark:border-gray-700 w-100">
              <template #title>{{ recipe.name }}</template>
              <template #header>
                <img :src="recipe.thumbnail_image_url" alt="" class="object-cover object-center w-full" />
              </template>
              <template #subtitle>
                <div class="flex items-center flex-col">
                  <Rating v-model="recipe.avg_rating" :readonly="true" v-tooltip="`${recipe.num_ratings} ratings`"/>
                  <div class="mt-2">
                    <Tag :value="category.name" severity="secondary" v-for="category in recipe.categories" />
                  </div>
                </div>
              </template>
            </Card>
          </Link>
        </div>
      </template>
    </DataView>
  </div>
</template>
