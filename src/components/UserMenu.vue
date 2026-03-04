<script setup lang="ts">
import type { User } from "@/types/users.ts";

import { ref } from "vue";
import { useI18n } from "vue-i18n";

import { useClickOutside } from "@/composables/click-outside.ts";

import UserAvatar from "@/components/UserAvatar.vue";

defineProps<{ user: User }>();
const isOpen = ref<boolean>(false);
const menuRef = ref<HTMLElement>();

useClickOutside(menuRef, () => (isOpen.value = false));

const { t } = useI18n();
</script>

<template>
  <div
    ref="menuRef"
    class="relative"
  >
    <user-avatar
      :user="user"
      aria-controls="user_menu"
      class="dropdown-toggle cursor-pointer"
      aria-haspopup="menu"
      aria-expanded="false"
      aria-label="Dropdown"
      size="lg"
      @click="isOpen = !isOpen"
    />
    <ul
      v-if="isOpen"
      class="absolute right-0 z-50 bg-base-100 border border-base-content/20 rounded-md shadow-lg max-h-60 overflow-y-auto w-fit max-w-fit"
      role="menu"
    >
      <li>
        <a
          class="dropdown-item"
          :href="t('routes.admin')"
        >
          <span class="icon-[wpf--administrator]"></span>
          {{ t("global.admin") }}
        </a>
      </li>
      <li>
        <a
          class="dropdown-item"
          :href="t('routes.logout')"
        >
          <span class="icon-[material-symbols--logout]"></span>
          {{ t("global.logout") }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style>
.language-selector button:not(:last-child)::after {
  content: "/";
}
</style>
