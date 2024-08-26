<script setup lang="ts">
import type { Category, CategoryType } from "@/types/categories";

import { Link } from "@inertiajs/vue3";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import BreadcrumbBar from "@/components/BreadcrumbBar.vue";
import SquareImage from "@/components/SquareImage.vue";
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
    <DataView
      layout="grid"
      :value="filteredCategories"
      data-key="slug"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between">
          <IconField class="w-full sm:w-auto">
            <InputIcon class="pi pi-search" />
            <InputText
              v-model="search"
              :placeholder="t('search.search')"
              class="w-full sm:w-auto"
            />
          </IconField>
        </div>
      </template>
      <template #grid="{ items }">
        <div
          class="grid auto-rows-fr grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 md:gap-8 p-4"
        >
          <Link
            v-for="category in items"
            :key="category.slug"
            :href="t('routes.category_detail', { slug: category.slug })"
            class="inline-grid"
          >
            <Card
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-full"
            >
              <template #header>
                <SquareImage :src="category.thumbnail_image_url" />
              </template>
              <template #title>
                <h2>{{ category.name_plural || category.name }}</h2>
              </template>
            </Card>
          </Link>
        </div>
      </template>
      <template #empty>
        <div class="flex items-center">
          <div class="p-4 w-full text-center">{{ t("categories.no_match") }}</div>
        </div>
      </template>
    </DataView>
  </div>
</template>
