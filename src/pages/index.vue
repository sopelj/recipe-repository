<script setup lang="ts">
import { User } from "../types/users.ts";

defineProps<{ user?: User }>();
</script>

<template>
  <div class="text-center h-screen flex justify-center flex-col items-center p-4">
    <h1 class="text-3xl font-bold" v-if="user">Welcome {{ user.first_name }}</h1>
    <h1 v-else>Welcome. Please Login!</h1>
    <h2 class="text-green-600 mb-5">This is still an empty project</h2>
  </div>
</template>
