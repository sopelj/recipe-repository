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
      <i class="pi pi-globe"></i>&nbsp;
      <a
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
      <i class="pi pi-book"></i>&nbsp;
      <meta
        itemprop="isbn"
        :content="source.value"
      />
      <a
        :href="`https://isbnsearch.org/search?s=${source.value}`"
        itemprop="name"
      >
        {{ source.name }}<span v-if="value">{{ t("source.page", { page: value }) }}</span>
      </a>
    </div>
    <div v-else-if="source.type === 3">
      <i class="pi pi-user"></i>&nbsp;
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
