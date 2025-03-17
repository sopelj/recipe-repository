<script setup lang="ts">
import type { User } from "@/types/users";

import { Link, router } from "@inertiajs/vue3";
import { type ComponentInstance, computed, ref } from "vue";
import { useI18n } from "vue-i18n";

import Menu from "primevue/menu";
import UserAvatar from "@/components/UserAvatar.vue";

const props = defineProps<{ user?: User }>();
const { t, locale } = useI18n();
const userMenu = ref<ComponentInstance<typeof Menu>>();
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
    <header class="w-full mb-4 bg-purple-900/75 text-white sticky top-0 backdrop-blur-sm shadow-lg z-50">
      <nav class="container mx-auto flex flex-row">
        <div class="flex-grow">
          <Link
            :href="t('routes.recipe_list')"
            class="flex flex-row py-2 items-center"
          >
            <Image
              src="/static/recipe-logo.svg"
              alt=""
              class="w-14 sm:w-10"
            />
            <span class="cursive text-3xl pl-2 hidden sm:inline-block">{{ t("global.title") }}</span>
            <span class="cursive text-2xl pl-2 sm:hidden">{{ t("global.title_short") }}</span>
          </Link>
        </div>
        <div class="flex items-center text-right gap-2">
          <div class="language-selector">
            <Button
              v-if="locale !== 'en'"
              link
              class="text-white p-0"
              @click="setLocale('en')"
            >
              <span class="sm:hidden">EN</span>
              <span class="hidden sm:inline-block">English</span>
            </Button>
            <Button
              v-if="locale !== 'fr'"
              link
              class="text-white p-0"
              @click="setLocale('fr')"
            >
              <span class="sm:hidden">FR</span>
              <span class="hidden sm:inline-block">Français</span>
            </Button>
            <Button
              v-if="locale !== 'ja'"
              link
              class="text-white p-0"
              @click="setLocale('ja')"
            >
              日本語
            </Button>
          </div>
          <Link
            v-if="!user"
            :href="t('routes.login')"
          >
            {{ t("global.login") }}
          </Link>
          <div
            v-else
            class="card flex justify-center"
          >
            <UserAvatar
              :user="user"
              aria-haspopup="true"
              aria-controls="user_menu"
              class="p-1"
              @click="toggleMenu"
            />
            <Menu
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
.language-selector button:not(:last-child)::after {
  content: "/";
}
</style>
