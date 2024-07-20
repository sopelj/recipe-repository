<script setup lang="ts">
import { Recipe } from "../types/recipes";

defineProps<{ recipe: Recipe }>();
</script>

<template>
  <div class="container mx-auto">
    <h1>{{ recipe.name }}</h1>
    <div>
      {{ recipe }}
    </div>
  </div>
</template>
