<script setup lang="ts">
import type { Source } from "@/types/recipes";

import { useI18n } from "vue-i18n";

defineProps<{ source: Source; value?: string }>();
const { t } = useI18n();
</script>

<template>
  <div
    itemprop="isBasedOn"
    itemscope
    itemtype="https://schema.org/CreativeWork"
  >
    <div v-if="source.type === 1">
      <link
        itemprop="url"
        :href="value"
      />
      <i class="icon-[humbleicons--globe]"></i>&nbsp;
      <a
        :title="t('source.visit_source_website')"
        :href="value"
        itemprop="publisher"
        target="_blank"
        class="underline"
        >{{ source.name }}</a
      >
    </div>
    <div
      v-else-if="source.type === 2"
      itemscope
      itemtype="https://schema.org/Book"
    >
      <i class="icon-[solar--book-bold]"></i>&nbsp;
      <meta
        itemprop="isbn"
        :content="source.value"
      />
      <a
        :title="t('source.lookup_book_info')"
        :href="`https://isbnsearch.org/search?s=${source.value}`"
        itemprop="name"
      >
        <template v-if="value">{{ t("source.book_page", { book: source.name, page: value }) }}</template>
        <template v-else>{{ source.name }}</template>
      </a>
    </div>
    <div v-else-if="source.type === 3">
      <i class="icon-[mdi--user]"></i>&nbsp;
      <span
        itemprop="author"
        itemscope
        itemtype="https://schema.org/Person"
        >{{ source.value }}</span
      >
    </div>
    <div v-else>
      {{ source.name }}
    </div>
  </div>
</template>
