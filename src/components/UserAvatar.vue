<script setup lang="ts">
import type { User } from "../types/users";

withDefaults(defineProps<{ user: User; size?: "normal" | "large" | "xlarge" }>(), { size: "large" });
</script>

<template>
    <avatar
      :image="user.profile_image_url ? user.profile_image_url : undefined"
      :label="user.profile_image_url ? undefined : user.initials"
      :size="size"
      shape="circle"
      class="mr-2"
    />
</template>
