<script setup lang="ts">
import type { Category } from "@/types/categories";
import type { RecipeItem } from "@/types/recipes";
import type { User } from "@/types/users";

import { Link } from "@inertiajs/vue3";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import ImportModal from "@/components/ImportModal.vue";
import MultiSelect from "@/components/MultiSelect.vue";
import RatingInput from "@/components/RatingInput.vue";
import SearchableLinkCards from "@/components/SearchableLinkCards.vue";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{
  user: User;
  recipes: RecipeItem[];
  category: Category | null;
  categories: Category[] | null;
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
const modalOpen = ref(false);
</script>

<template>
  <head-section :title="title" />
  <div class="container mx-auto">
    <div class="flex flex-wrap items-center">
      <h1
        class="text-2xl pt-2 pb-4 px-4 grow w-full sm:w-auto"
        :style="category ? `view-transition-name: category-${category.slug}-name` : ''"
      >
        {{ title }}
      </h1>
      <div class="mx-4 w-full flex mb-2 grow sm:grow-0 sm:w-auto sm:mx-0 sm:mb-0">
        <Link
          v-if="user"
          class="btn btn-outline mr-2 px-2"
          :title="t('recipe.add')"
          :href="t('routes.recipe_add')"
        >
          <span class="icon-[ic--baseline-plus]"></span>
        </Link>
        <button
          v-if="user"
          class="btn btn-outline mr-2 px-2"
          :title="t('recipe.import')"
          @click="modalOpen = true"
        >
          <span class="icon-[iconoir--import]"></span>
        </button>
        <span class="grow sm:grow-0"></span>
        <Link
          v-if="!category"
          :href="t('routes.category_type_list')"
          class="btn btn-outline md:mr-4 lg:mr-0"
        >
          {{ t("recipe.browse_categories") }}
        </Link>
      </div>
    </div>
    <breadcrumb-bar
      :items="breadcrumbItems"
      class="px-4"
    />
    <searchable-link-cards
      v-model:search="search"
      :grid-items="filteredRecipes"
      :no-results-message="t('search.no_recipes_match')"
      route-name="recipe_detail"
      type="recipe"
    >
      <template #extra-inputs>
        <multi-select
          v-if="categories"
          v-model="selectedCategories"
          :options="categoryOptions"
          :placeholder="t('search.select_category')"
          class="join-item"
          select-class="rounded-l-none"
        />
      </template>
      <template #extra-card-content="{ item }">
        <rating-input
          v-model="item.avg_rating"
          :title="t('recipe.ratings', item.num_ratings)"
          :readonly="true"
          :size="4"
          class="mt-1"
        />
      </template>
    </searchable-link-cards>
  </div>
  <import-modal v-model="modalOpen" />
</template>
