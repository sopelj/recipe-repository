<script setup lang="ts" generic="T extends GridItem">
import type { GridItem } from "@/types/common.ts";

import { Link } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import SquareImage from "@/components/SquareImage.vue";

const search = defineModel<string>("search");

defineProps<{ gridItems: T[]; routeName: string; type: string; noResultsMessage: string }>();

const { t } = useI18n();
</script>

<template>
  <div class="relative px-4">
    <div class="pl-2 border rounded-md join h-10 w-full max-w-full sm:w-auto">
      <span
        class="icon-[heroicons--magnifying-glass] text-base-content/80 my-auto me-3 size-5 shrink-0 join-item"
      ></span>
      <label
        class="sr-only"
        for="search-input"
      >
        {{ t("search.search") }}
      </label>
      <input
        id="search-input"
        v-model="search"
        type="text"
        class="join-item grow"
        :placeholder="t('search.search')"
      />
      <slot name="extra-inputs" />
    </div>
    <template v-if="gridItems.length > 0">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 py-4">
        <Link
          v-for="gridItem in gridItems"
          :key="gridItem.slug"
          :href="t(`routes.${routeName}`, { slug: gridItem.slug })"
          class="inline-grid rounded-md"
          :style="`view-transition-name: ${type}-${gridItem.slug}-name`"
          view-transition
        >
          <div class="card text-center overflow-clip transition-all hover:scale-105 w-full">
            <div class="card-header">
              <square-image
                :src="gridItem.thumbnail_url"
                :style="`view-transition-name: ${type}-${gridItem.slug}-image`"
              />
            </div>
            <div class="card-body p-2 flex grow flex-wrap justify-center">
              <h2 class="grow text-sm w-full">{{ gridItem?.name_plural || gridItem.name }}</h2>
              <slot
                name="extra-card-content"
                :item="gridItem"
              />
            </div>
          </div>
        </Link>
      </div>
    </template>
    <template v-else>
      <div class="flex items-center">
        <div class="p-4 w-full text-center">{{ noResultsMessage }}</div>
      </div>
    </template>
  </div>
</template>
