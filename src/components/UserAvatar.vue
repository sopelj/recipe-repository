<script setup lang="ts">
import { computed } from "vue";

import type { User } from "../types/users";

const props = withDefaults(defineProps<{ user: User; size?: keyof typeof sizes }>(), { size: "md" });

const sizes = {
  sm: "size-6",
  md: "size-8",
  lg: "size-10",
};

const sizeClass = computed(() => {
  return sizes[props.size];
});
</script>

<template>
  <div
    class="avatar"
    :title="user.full_name"
  >
    <div
      class="flex items-center justify-center rounded-full border"
      :class="sizeClass"
    >
      <img
        v-if="user.profile_image_url"
        :src="user.profile_image_url"
        alt="avatar"
      />
      <div
        v-else
        class="text-center"
        style="font-size: 1em; line-height: 1em"
      >
        {{ user.initials }}
      </div>
    </div>
  </div>
</template>
