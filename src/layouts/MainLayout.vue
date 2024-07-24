<script setup lang="ts">
import type { User } from "../types/users.ts";

import { Link as ILink } from "@inertiajs/vue3"
import PToolbar from "primevue/toolbar";
import PAvatar from "primevue/avatar";
import PMenu from "primevue/menu";
import PImage from "primevue/image";

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
</script>

<template>
  <main>
    <header class="container mx-auto my-2 mb-4">
      <p-toolbar class="py-1">
        <template #start>
          <div class="flex items-center">
            <i-link href="/en/" class="flex flex-row py-2 items-center">
              <p-image src="/static/images/recipe-logo.svg" alt="" :width="50" />
              <div class="cursive text-3xl pl-2">Recipe Repo<span>sitory</span></div>
            </i-link>
          </div>
        </template>
        <template #end>
          <div class="flex items-center gap-2">
            <i-link v-if="!user" href="/admin/login/">Login</i-link>
            <div v-else class="card flex justify-center">
              <p-avatar :image="user.profile_image_url || ''" size="large" shape="circle" aria-haspopup="true" aria-controls="user_menu"  @click="toggleMenu"/>
              <p-menu id="user_menu" ref="userMenu" :model="userMenuItems"  :popup="true" class="items-end" />
            </div>
          </div>
        </template>
      </p-toolbar>
    </header>
    <article>
      <slot />
    </article>
  </main>
</template>
