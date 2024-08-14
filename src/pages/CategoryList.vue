<script setup lang="ts">
import type { Category } from "@/types/categories";

import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import { Link as ILink } from "@inertiajs/vue3";
import HeadSection from "@/layouts/HeadSection.vue";

const props = defineProps<{ parentCategories?: Category[]; categories: Category[] }>();
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
    <div class="flex items-center">
      <h1 class="text-4xl pt-2 pb-4 px-4 flex-grow">{{ t("categories.all_categories") }}</h1>
      <ILink
        :href="t('routes.recipe_list')"
        class="pr-2 sm:pr-0 text-center hover:underline"
      >
        {{ t("recipe.all_recipes") }}
      </ILink>
    </div>
    <DataView
      layout="grid"
      :value="filteredCategories"
      data-key="slug"
    >
      <template #header>
        <div class="flex flex-wrap items-center justify-between">
          <icon-field class="w-full sm:w-auto">
            <input-icon class="pi pi-search" />
            <input-text
              v-model="search"
              :placeholder="t('search.search')"
              class="w-full sm:w-auto"
            />
          </icon-field>
        </div>
      </template>
      <template #grid="{ items }">
        <div class="grid grid-cols-12 gap-4">
          <ILink
            v-for="category in items"
            :key="category.slug"
            :href="t('routes.recipe_category', { slug: category.slug })"
            class="col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <Card
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-100"
            >
              <template #title>
                <h2>{{ category.name_plural || category.name }}</h2>
              </template>
              <template #header>
                <img
                  :src="category.thumbnail_image_url"
                  alt=""
                  class="object-cover object-center w-full"
                />
              </template>
            </Card>
          </ILink>
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
