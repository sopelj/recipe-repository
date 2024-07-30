<script setup lang="ts">
import type { Category } from "../types/categories";

import PCard from "primevue/card";
import PImage from "primevue/image";
import DataView from "primevue/dataview";
import { computed, ref } from "vue";
import { Link as ILink } from "@inertiajs/vue3";

const props = defineProps<{ parentCategories?: Category[], categories: Category[] }>();
const search = ref<string>("");
const filteredCategories = computed((): Category[] => (
    search.value ? props.categories.filter((c) => !c.name.toLocaleLowerCase().search(search.value.toLocaleLowerCase())) : props.categories)
);
</script>

<template>
  <div class="container mx-auto">
    <h1 class="sr-only">Categories</h1>
    <data-view layout="grid" :value="filteredCategories" data-key="slug">
      <template #header>
        <div class="flex justify-end">
          <icon-field>
            <input-icon class="pi pi-search" />
            <input-text v-model="search" placeholder="Search" />
          </icon-field>
        </div>
      </template>
      <template #grid="{ items }">
        <div class="grid grid-cols-12 gap-4">
          <i-link
              v-for="category in items"
              :key="category.slug"
              :href="`/categories/${category.slug}/`"
              class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 xl:col-span-2 p-2"
          >
            <p-card class="text-center rounded-md overflow-clip border-solid border-2 dark:border-gray-700 w-100">
              <template #title>{{ category.name_plural || category.name }}</template>
              <template #header>
                <p-image :src="category.thumbnail_image_url" alt="" class="object-cover object-center w-full" />
              </template>
            </p-card>
          </i-link>
        </div>
      </template>
    </data-view>
  </div>
</template>