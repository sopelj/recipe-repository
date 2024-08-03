<script setup lang="ts">
import type { Category } from "../types/categories";

import PCard from "primevue/card";
import PImage from "primevue/image";
import DataView from "primevue/dataview";
import { computed, ref } from "vue";
import { Link as ILink } from "@inertiajs/vue3";
import HeadSection from "../layouts/HeadSection.vue";
import { useI18n } from "vue-i18n";

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
  <HeadSection title="categories" />
  <div class="container mx-auto">
    <h1 class="sr-only">{{ t("categories.title") }}</h1>
    <DataView
      layout="grid"
      :value="filteredCategories"
      data-key="slug"
    >
      <template #header>
        <div class="flex justify-end">
          <icon-field>
            <input-icon class="pi pi-search" />
            <input-text
              v-model="search"
              :placeholder="t('search.search')"
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
            class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <PCard
              class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-100"
            >
              <template #title>{{ category.name_plural || category.name }}</template>
              <template #header>
                <PImage
                  :src="category.thumbnail_image_url"
                  alt=""
                  class="object-cover object-center w-full"
                />
              </template>
            </PCard>
          </ILink>
        </div>
      </template>
    </DataView>
  </div>
</template>
