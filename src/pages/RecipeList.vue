<script setup lang="ts">
import type { Category } from "@/types/categories";
import type { RecipeItem } from "@/types/recipes";

import { Link } from "@inertiajs/vue3";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import SquareImage from "@/components/SquareImage.vue";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{
  recipes: RecipeItem[];
  "category": Category | null;
  "categories": Category[] | null;
}>();
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
  props.categories?.map((c) => ({ label: c.name_plural || c.name, value: c.slug })),
);
const selectedCategories = ref<string[]>([]);
const title = computed(
  (): string => props.category?.name_plural || props.category?.name || t("recipe.all_recipes"),
);
const breadcrumbItems = computed(() =>
  props?.category
    ? [
        { label: t("categories.category_types"), url: t("routes.category_type_list") },
        {
          label: props.category.type.name_plural || props.category.type.name,
          url: t("routes.category_type_detail", { slug: props.category.type.slug }),
        },
        { label: title.value },
      ]
    : [],
);
</script>

<template>
  <HeadSection :title="title" />
  <div class="container mx-auto">
    <div class="flex items-center">
      <h1 class="text-4xl pt-2 pb-4 px-4 flex-grow">{{ title }}</h1>
      <Link
        v-if="!category"
        :href="t('routes.category_type_list')"
        class="text-center pr-2 sm:pr-0 hover:underline"
      >
        {{ t("recipe.browse_categories") }}
      </Link>
    </div>
    <BreadcrumbBar :items="breadcrumbItems" />
    <DataView
      layout="grid"
      :value="filteredRecipes"
      data-key="slug"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between">
          <IconField class="w-full sm:w-auto mb-3 sm:mb-0">
            <InputIcon class="pi pi-search" />
            <InputText
              v-model="search"
              :placeholder="t('search.search')"
              class="w-full sm:w-auto"
            />
          </IconField>
          <MultiSelect
            v-if="categories"
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
        <div
          class="grid auto-rows-fr grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 md:gap-8 p-4"
        >
          <Link
            v-for="recipe in items"
            :key="recipe.slug"
            :href="t('routes.recipe_details', { slug: recipe.slug })"
            class="inline-grid"
          >
            <Card
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-full"
              :pt="{ body: 'h-full', content: 'h-full flex flex-col items-center justify-center' }"
            >
              <template #header>
                <SquareImage :src="recipe.thumbnail_url" />
              </template>
              <template #content>
                <h2 class="mb-1">{{ recipe.name }}</h2>
                <Rating
                  v-model="recipe.avg_rating"
                  v-tooltip="t('recipe.ratings', recipe.num_ratings)"
                  :readonly="true"
                />
              </template>
            </Card>
          </Link>
        </div>
      </template>
      <template #empty>
        <div class="flex items-center">
          <div class="p-4 w-full text-center">{{ t("search.no_recipes_match") }}</div>
        </div>
      </template>
    </DataView>
  </div>
</template>
