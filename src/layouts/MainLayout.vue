<script setup lang="ts">
import type { User } from "../types/users.ts";

import { Link as ILink, router } from "@inertiajs/vue3";
import PMenu from "primevue/menu";
import PButton from "primevue/button";

import { ref, type ComponentInstance, computed } from "vue";
import { useI18n } from "vue-i18n";

const props = defineProps<{ user?: User }>();
const { t, locale } = useI18n();
const userMenu = ref<ComponentInstance<typeof PMenu>>();
const toggleMenu = (event: Event) => {
  userMenu.value?.toggle(event);
};
const userMenuItems = computed(() => {
  const items = [{ label: t("global.logout"), icon: "pi pi-sign-out", url: t("routes.logout") }];
  if (props.user?.is_staff) {
    return [{ label: t("global.admin"), icon: "pi pi-pen-to-square", url: t("routes.admin") }, ...items];
  }
  return items;
});
const setLocale = (lang: string) => {
  locale.value = lang;
  router.visit(t("routes.recipe_list"));
};
</script>

<template>
  <main :lang="locale">
    <header class="w-100 mb-4 bg-purple-900/75 text-white sticky top-0 backdrop-blur-sm shadow-lg">
      <nav class="container mx-auto flex flex-row">
        <div class="flex-grow">
          <ILink
            :href="t('routes.recipe_list')"
            class="flex flex-row py-2 items-center"
          >
            <image
              src="/static/images/recipe-logo.svg"
              alt=""
              :width="50"
            />
            <div class="cursive text-3xl pl-2">{{ t("global.title") }}</div>
          </ILink>
        </div>
        <div class="flex items-center gap-2">
          <div class="language-selector">
            <PButton
              v-if="locale !== 'en'"
              link
              @click="setLocale('en')"
              >English</PButton
            >
            <PButton
              v-if="locale !== 'fr'"
              link
              @click="setLocale('fr')"
              >Français</PButton
            >
            <PButton
              v-if="locale !== 'ja'"
              link
              @click="setLocale('ja')"
              >日本語</PButton
            >
          </div>
          <ILink
            v-if="!user"
            :href="t('routes.login')"
            >{{ t("global.login") }}</ILink
          >
          <div
            v-else
            class="card flex justify-center"
          >
            <avatar
              :image="user.profile_image_url || ''"
              size="large"
              shape="circle"
              aria-haspopup="true"
              aria-controls="user_menu"
              @click="toggleMenu"
            />
            <PMenu
              id="user_menu"
              ref="userMenu"
              :model="userMenuItems"
              :popup="true"
              class="items-end"
            />
          </div>
        </div>
      </nav>
    </header>
    <article>
      <slot />
    </article>
  </main>
</template>

<style>
.language-selector a:not(:last-child)::after {
  content: " / ";
}
</style>
