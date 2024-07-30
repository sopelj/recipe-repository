<script setup lang="ts">
import type { User } from "../types/users.ts";

import { Link as ILink } from "@inertiajs/vue3"
import PMenu from "primevue/menu";

import { ref, type ComponentInstance, computed } from "vue";

const props = defineProps<{ user?: User }>();

const userMenu = ref<ComponentInstance<typeof PMenu>>();
const toggleMenu = (event: Event) => {
  userMenu.value?.toggle(event);
}
const userMenuItems = computed(() => {
  const items = [{ label: 'Logout', icon: 'pi pi-sign-out', url: '/en/admin/logout/'}];
  if (props.user?.is_staff) {
    return [{label: 'Admin', icon: 'pi pi-pen-to-square', url: '/en/admin/'}, ...items];
  }
  return items;
})
const locale = computed((): string => document.documentElement.lang);
</script>

<template>
  <main>
    <header class="w-100 mb-4 bg-purple-900/75 text-white sticky top-0 backdrop-blur-sm shadow-lg">
      <nav class="container mx-auto flex flex-row">
          <div class="flex-grow">
            <i-link :href="`/${locale}/`" class="flex flex-row py-2  items-center">
              <Image src="/static/images/recipe-logo.svg" alt="" :width="50" />
              <div class="cursive text-3xl pl-2">Recipe Repo<span>sitory</span></div>
            </i-link>
          </div>
          <div class="flex items-center gap-2">
            <div class="language-selector">
              <i-link v-if="locale !== 'en'" href="/en/">English</i-link>
              <i-link v-if="locale !== 'fr'"  href="/fr/">Français</i-link>
              <i-link v-if="locale !== 'ja'" href="/ja/">日本語</i-link>
            </div>
            <i-link v-if="!user" href="/admin/login/">Login</i-link>
            <div v-else class="card flex justify-center">
              <avatar :image="user.profile_image_url || ''" size="large" shape="circle" aria-haspopup="true" aria-controls="user_menu"  @click="toggleMenu"/>
              <p-menu id="user_menu" ref="userMenu" :model="userMenuItems"  :popup="true" class="items-end" />
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
