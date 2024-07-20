<script setup lang="ts">
import type { Category } from "../types/categories";

import Card from "primevue/card";
import Image from 'primevue/image';

defineProps<{ categories: Category[] }>();
</script>

<template>
  <div class="container mx-auto">
    <h1>Categories</h1>
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
