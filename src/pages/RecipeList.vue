<script setup lang="ts">
import type { RecipeItem } from "../types/recipes";
import type { Category } from "../types/categories.ts";

import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import { Link as ILink } from "@inertiajs/vue3";
import HeadSection from "../layouts/HeadSection.vue";

const props = defineProps<{ recipes: RecipeItem[]; "category"?: Category; "categories": Category[] }>();
const { t } = useI18n();
const search = ref<string>("");
const filteredRecipes = computed((): RecipeItem[] =>
  props.recipes.filter(
    (r: RecipeItem) =>
      (!search.value || !r.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase())) &&
      (!selectedCategories.value?.length ||
        r.categories?.some((c: Category) => selectedCategories.value.includes(c.slug))),
  ),
);
const categoryOptions = computed(() =>
  props.categories.map((c) => ({ label: c.name_plural || c.name, value: c.slug })),
);
const selectedCategories = ref<string[]>([]);
const title = computed(
  (): string => props.category?.name_plural || props.category?.name || t("recipe.all_recipes"),
);
</script>

<template>
  <HeadSection :title="title" />
  <div class="container mx-auto">
    <h1 class="text-4xl pt-2 pb-4 px-4">{{ title }}</h1>
    <data-view
      layout="grid"
      :value="filteredRecipes"
      data-key="slug"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between">
          <icon-field class="w-full sm:w-auto mb-3 sm:mb-0">
            <input-icon class="pi pi-search" />
            <input-text
              v-model="search"
              :placeholder="t('search.search')"
              class="w-full sm:w-auto"
            />
          </icon-field>
          <multi-select
            v-model="selectedCategories"
            :options="categoryOptions"
            :placeholder="t('search.select_category')"
            option-value="value"
            option-label="label"
            display="chip"
            class="w-full sm:w-auto"
          />
        </div>
      </template>
      <template #grid="{ items }">
        <div class="grid grid-cols-12 gap-4 p-4">
          <ILink
            v-for="recipe in items"
            :key="recipe.slug"
            :href="t('routes.recipe_details', { slug: recipe.slug })"
            class="col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <card
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-100"
            >
              <template #title
                ><h2>{{ recipe.name }}</h2></template
              >
              <template #header>
                <img
                  :src="recipe.thumbnail_image_url"
                  alt=""
                  class="object-cover object-center w-full"
                />
              </template>
              <template #subtitle>
                <div class="flex items-center flex-col">
                  <Rating
                    v-model="recipe.avg_rating"
                    v-tooltip="t('recipe.ratings', recipe.num_ratings)"
                    :readonly="true"
                  />
                  <div class="mt-2">
                    <tag
                      v-for="c in recipe.categories"
                      :key="c.slug"
                      :value="c.name"
                      class="m-1"
                      severity="secondary"
                    />
                  </div>
                </div>
              </template>
            </card>
          </ILink>
        </div>
      </template>
      <template #empty>
        <div class="flex items-center">
          <div class="p-4 w-full text-center">{{ t("search.no_recipes_match") }}</div>
        </div>
      </template>
    </data-view>
  </div>
</template>
