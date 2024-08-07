<script setup lang="ts">
import type { User } from "../types/users";

withDefaults(defineProps<{ user: User; size?: "normal" | "large" | "xlarge" }>(), { size: "large" });
</script>

<template>
  <Avatar
    :image="user.profile_image_url ? user.profile_image_url : undefined"
    :icon="user.profile_image_url ? undefined : 'pi pi-user'"
    :size="size"
    shape="circle"
    class="mr-2"
  />
</template>
