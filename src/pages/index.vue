<script setup lang="ts">
import Card from "primevue/card";
import Image from 'primevue/image';
import { Category, User } from "../types/users.ts";

defineProps<{ user?: User, categories: Category[] }>();
</script>

<template>
  <div class="text-center h-screen flex justify-center flex-col items-center p-4">
    <h1 class="text-3xl font-bold" v-if="user">Welcome {{ user.first_name }}</h1>
    <h1 v-else>Welcome. Please Login!</h1>
    <h2>Categories</h2>
    <div>
      <Card v-for="category in categories">
        <template #title>{{ category.name_plural }}</template>
        <template #header>
          <Image :src="category.thumbnail_image_url" alt="" />
        </template>
      </Card>
    </div>
  </div>
</template>
