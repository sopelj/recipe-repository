<script setup lang="ts">
import type { MenuItem } from "primevue/menuitem";

import { Link } from "@inertiajs/vue3";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

const props = withDefaults(defineProps<{ items?: MenuItem[]; current?: string }>(), {
  items: () => [],
  current: undefined,
});

const { t } = useI18n();
const home = { url: t("routes.recipe_list"), label: t("recipe.all_recipes") };
const crumbs = computed(() => [...props.items, ...(props.current ? [{ label: props.current }] : [])]);
</script>

<template>
  <Breadcrumb
    :home="home"
    :model="crumbs"
    :pt="{ list: 'flex-wrap' }"
    class="bg-transparent"
  >
    <template #item="{ item }">
      <Link
        v-if="item.url"
        :href="item.url"
      >
        <span :class="[item.icon, 'text-color']" />
        <span class="text-primary font-semibold">{{ item.label }}</span>
      </Link>
      <span v-else>
        <span :class="[item.icon, 'text-color']" />
        <span class="font-semibold text-slate-400">{{ item.label }}</span>
      </span>
    </template>
    <template #separator>/</template>
  </Breadcrumb>
</template>
