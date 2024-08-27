<script setup lang="ts" generic="T extends GridItem">
import type { GridItem } from "@/types/common.ts";

import { Link } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import SquareImage from "@/components/SquareImage.vue";

const search = defineModel<string>("search");

defineProps<{ gridItems: T[]; routeName: string; noResultsMessage: string }>();

const { t } = useI18n();
</script>

<template>
  <DataView
    layout="grid"
    :value="gridItems"
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
        <slot name="extra-header" />
      </div>
    </template>
    <template #grid="{ items }">
      <div
        class="grid auto-rows-fr grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 md:gap-8 p-4"
      >
        <Link
          v-for="gridItem in items"
          :key="gridItem.slug"
          :href="t(`routes.${routeName}`, { slug: gridItem.slug })"
          class="inline-grid"
        >
          <Card
            class="text-center overflow-clip transition-all border dark:border-slate-600 dark:hover:border-violet-700 hover:scale-105 w-full"
            :pt="{ body: 'h-full', content: 'h-full flex flex-col items-center justify-center' }"
          >
            <template #header>
              <SquareImage :src="gridItem.thumbnail_url" />
            </template>
            <template #content>
              <h2>{{ gridItem?.name_plural || gridItem.name }}</h2>
              <slot
                name="extra-card-content"
                :item="gridItem"
              />
            </template>
          </Card>
        </Link>
      </div>
    </template>
    <template #empty>
      <div class="flex items-center">
        <div class="p-4 w-full text-center">{{ noResultsMessage }}</div>
      </div>
    </template>
  </DataView>
</template>
