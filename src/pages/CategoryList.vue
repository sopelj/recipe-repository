<script setup lang="ts">
import Card from "primevue/card";
import Image from 'primevue/image';
import { Category, User } from "../types/users.ts";

defineProps<{ user?: User, categories: Category[] }>();
</script>

<template>
  <div class="container mx-auto">
    <h1 class="text-3xl font-bold" v-if="user">Welcome {{ user.first_name }}</h1>
    <h1 v-else>Welcome. Please Login!</h1>
    <h2>Categories</h2>
    <div class="grid gap-4 grid-flow-col auto-cols-[minmax(0,_2fr)]">
      <Card v-for="category in categories" class="text-center w-100">
        <template #title>{{ category.name_plural }}</template>
        <template #header>
          <Image :src="category.thumbnail_image_url" alt="" />
        </template>
      </Card>
    </div>
  </div>
</template>
