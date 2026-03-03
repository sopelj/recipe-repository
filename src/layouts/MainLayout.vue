<script setup lang="ts">
import type { User } from "@/types/users";

import { Link, router } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import UserMenu from "@/layouts/UserMenu.vue";

defineProps<{ user?: User }>();
const { t, locale } = useI18n();
const setLocale = (lang: string) => {
  locale.value = lang;
  router.visit(t("routes.recipe_list"));
};
</script>

<template>
  <main :lang="locale">
    <header class="w-full mb-4 bg-purple-900/75 text-white sticky top-0 backdrop-blur-sm shadow-lg z-50">
      <nav class="container mx-auto flex flex-row">
        <div class="grow">
          <Link
            :href="t('routes.recipe_list')"
            class="flex flex-row py-2 items-center"
          >
            <img
              src="/assets/recipe-logo.svg"
              alt=""
              class="w-14 sm:w-10"
            />
            <span class="cursive text-2xl pl-2 hidden sm:inline-block">{{ t("global.title") }}</span>
            <span class="cursive text-xl pl-2 sm:hidden">{{ t("global.title_short") }}</span>
          </Link>
        </div>
        <div class="flex items-center text-right gap-2">
          <div class="language-selector">
            <button
              v-if="locale !== 'en'"
              class="btn-text text-white p-0 cursor-pointer"
              @click="setLocale('en')"
            >
              <span class="sm:hidden">EN</span>
              <span class="hidden sm:inline-block">English</span>
            </button>
            <button
              v-if="locale !== 'fr'"
              class="btn-text text-white p-0 cursor-pointer"
              @click="setLocale('fr')"
            >
              <span class="sm:hidden">FR</span>
              <span class="hidden sm:inline-block">Français</span>
            </button>
            <button
              v-if="locale !== 'ja'"
              class="btn-text text-white p-0 cursor-pointer"
              @click="setLocale('ja')"
            >
              日本語
            </button>
          </div>
          <user-menu
            v-if="user"
            :user="user"
          />
          <a
            v-else
            :href="t('routes.login')"
          >
            <span class="icon-[material-symbols--login]"></span>
            {{ t("global.login") }}
          </a>
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
