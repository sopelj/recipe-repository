<script setup lang="ts">
import { Link } from "@inertiajs/vue3"
import Toolbar from "primevue/toolbar";
import Avatar from "primevue/avatar";

import { User } from "../types/users.ts";

defineProps<{ user?: User }>()
</script>

<template>
  <main>
    <header>
      <Toolbar>
        <template #start>
          <div class="flex items-center gap-2">
            <Link href="/">
              <Image src="/static/images/recipe-logo.svg" alt="" :width="50" />
              <span class="flex">Recipes</span>
            </Link>
          </div>
        </template>
        <template #end>
          <div class="flex items-center gap-2">
            <Avatar v-if="user" :image="user.profile_image_url" size="large" shape="circle" />
            <Link v-else href="/admin/login/">Login</Link>
          </div>
        </template>
      </Toolbar>
    </header>
    <article>
      <slot />
    </article>
  </main>
</template>
