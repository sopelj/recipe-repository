<script setup lang="ts">
import type { CategoryType } from "@/types/categories";

import { Link } from "@inertiajs/vue3";
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import SquareImage from "@/components/SquareImage.vue";
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
    <div class="flex items-center">
      <h1 class="text-4xl pt-2 pb-4 px-4 flex-grow">{{ t("categories.all_category_types") }}</h1>
      <Link
        :href="t('routes.recipe_list')"
        class="pr-2 sm:pr-0 text-center hover:underline"
      >
        {{ t("recipe.all_recipes") }}
      </Link>
    </div>
    <DataView
      layout="grid"
      :value="filteredCategoryTypes"
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
            v-for="categoryType in items"
            :key="categoryType.slug"
            :href="t('routes.category_type_detail', { slug: categoryType.slug })"
            class="inline-grid"
          >
            <Card
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-full"
            >
              <template #header>
                <SquareImage :src="categoryType.thumbnail_image_url" />
              </template>
              <template #title>
                <h2>{{ categoryType.name_plural || categoryType.name }}</h2>
              </template>
            </Card>
          </Link>
        </div>
      </template>
      <template #empty>
        <div class="flex items-center">
          <div class="p-4 w-full text-center">{{ t("categories.type_no_match") }}</div>
        </div>
      </template>
    </DataView>
  </div>
</template>
