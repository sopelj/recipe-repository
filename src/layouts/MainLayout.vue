<script setup lang="ts">
import { Link } from "@inertiajs/vue3"
import Toolbar from "primevue/toolbar";
import Avatar from "primevue/avatar";
import Menu from "primevue/menu";

import { User } from "../types/users.ts";
import {ref, type ComponentInstance, computed} from "vue";

const props = defineProps<{ user?: User }>();

const userMenu = ref<ComponentInstance<typeof Menu>>();
const toggleMenu = (event: Event) => {
  userMenu.value.toggle(event);
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
      <Toolbar class="py-1">
        <template #start>
          <div class="flex items-center gap-2">
            <Link href="/en/">
              <Image src="/static/images/recipe-logo.svg" alt="" :width="50" />
              <span class="flex">Recipes</span>
            </Link>
          </div>
        </template>
        <template #end>
          <div class="flex items-center gap-2">
            <Link v-if="!user" href="/admin/login/">Login</Link>
            <div v-else class="card flex justify-center">
              <Avatar  :image="user.profile_image_url" size="large" shape="circle" @click="toggleMenu" aria-haspopup="true" aria-controls="user_menu" />
              <Menu ref="userMenu" :model="userMenuItems" id="user_menu" :popup="true" class="items-end">
                <template #item="{ item, props }">
                  <Link :href="item.url" v-bind="props.action">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                  </Link>
                </template>
              </Menu>
            </div>
          </div>
        </template>
      </Toolbar>
    </header>
    <article>
      <slot />
    </article>
  </main>
</template>
