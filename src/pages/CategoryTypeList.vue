<script setup lang="ts">
import type { CategoryType } from "@/types/categories";

import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import SearchableLinkCards from "@/components/SearchableLinkCards.vue";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{ categoryTypes: CategoryType[] }>();
const { t } = useI18n();

const search = ref<string>("");
const filteredCategoryTypes = computed((): CategoryType[] =>
  search.value
    ? props.categoryTypes.filter((c) => !c.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase()))
    : props.categoryTypes,
);
</script>

<template>
  <HeadSection :title="t('categories.title')" />
  <div class="container mx-auto">
    <h1 class="text-4xl pt-2 pb-4 px-4 flex-grow">{{ t("categories.all_category_types") }}</h1>
    <BreadcrumbBar :current="t('categories.all_category_types')" />
    <SearchableLinkCards
      v-model:search="search"
      :grid-items="filteredCategoryTypes"
      :no-results-message="t('categories.type_no_match')"
      route-name="category_type_detail"
    />
  </div>
</template>
