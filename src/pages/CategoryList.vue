<script setup lang="ts">
import type { Category, CategoryType } from "@/types/categories";

import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import SearchableLinkCards from "@/components/SearchableLinkCards.vue";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{ categoryType: CategoryType; categories: Category[] }>();
const { t } = useI18n();

const search = ref<string>("");
const filteredCategories = computed((): Category[] =>
  search.value
    ? props.categories.filter((c) => !c.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase()))
    : props.categories,
);
</script>

<template>
  <HeadSection :title="t('categories.title')" />
  <div class="container mx-auto">
    <h1 class="text-4xl pt-2 pb-4 px-4 flex-grow">{{ categoryType.name_plural || categoryType.name }}</h1>
    <BreadcrumbBar
      :items="[{ url: t('routes.category_type_list'), label: t('categories.category_types') }]"
      :current="categoryType.name_plural || categoryType.name"
    />
    <SearchableLinkCards
      v-model:search="search"
      :grid-items="filteredCategories"
      :no-results-message="t('categories.no_match')"
      route-name="category_detail"
    />
  </div>
</template>
