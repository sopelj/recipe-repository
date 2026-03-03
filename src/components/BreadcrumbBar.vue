<script setup lang="ts">
import { Link } from "@inertiajs/vue3";
import { computed } from "vue";
import { useI18n } from "vue-i18n";

interface MenuItem {
  label: string;
  url?: string;
  icon?: string;
}

const props = withDefaults(defineProps<{ items?: MenuItem[]; current?: string }>(), {
  items: () => [],
  current: undefined,
});

const { t } = useI18n();
const home = { url: t("routes.recipe_list"), label: t("recipe.all_recipes") };
const crumbs = computed((): MenuItem[] => [
  home,
  ...props.items,
  ...(props.current ? [{ label: props.current }] : []),
]);
</script>

<template>
  <div class="breadcrumbs">
    <ul class="flex flex-row mb-2">
      <li
        v-for="(crumb, index) in crumbs"
        :key="index"
        class="flex flex-row items-center"
      >
        <Link
          v-if="crumb.url"
          :href="crumb.url"
          view-transition
        >
          <span :class="[crumb?.icon || '', 'text-color']" />
          <span class="text-primary font-semibold">{{ crumb.label }}</span>
        </Link>
        <span v-else>
          <span :class="[crumb?.icon || '', 'text-color']" />
          <span class="font-semibold text-slate-400">{{ crumb.label }}</span>
        </span>
        <span
          v-if="index < crumbs.length - 1"
          class="icon-[tabler--chevron-right] breadcrumbs-separator rtl:rotate-180 mt-1"
        ></span>
      </li>
    </ul>
  </div>
</template>
