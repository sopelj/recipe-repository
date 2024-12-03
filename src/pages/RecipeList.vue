<script setup lang="ts">
import type { Category } from "@/types/categories";
import type { RecipeItem } from "@/types/recipes";

import { Link } from "@inertiajs/vue3";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import SearchableLinkCards from "@/components/SearchableLinkCards.vue";
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
      (!search.value || r.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase())) !== -1 &&
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
    <SearchableLinkCards
      v-model:search="search"
      :grid-items="filteredRecipes"
      :no-results-message="t('search.no_recipes_match')"
      route-name="recipe_detail"
    >
      <template #extra-header>
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
      </template>
      <template #extra-card-content="{ item }">
        <Rating
          v-model="item.avg_rating"
          v-tooltip="t('recipe.ratings', item.num_ratings)"
          :readonly="true"
        />
      </template>
    </SearchableLinkCards>
  </div>
</template>
