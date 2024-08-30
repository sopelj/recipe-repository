<script setup lang="ts">
import type { Comment } from "@/types/recipes";

import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import UserAvatar from "@/components/UserAvatar.vue";

defineProps<{ comments: Comment[]; collapse?: boolean }>();

const { t, d } = useI18n();

const form = useForm({ comment: "" });

const postComment = async () => {
  form.post(`${window.location.pathname}${window.location.search}`, {
    only: ["recipe"],
    preserveScroll: true,
  });
  form.reset();
};
</script>

<template>
  <Panel
    :collapsed="collapse"
    :toggleable="collapse"
  >
    <template #header>
      <h3>{{ t("comments.title") }}</h3>
    </template>
    <template #icons>
      <Badge>{{ comments.length }}</Badge>
    </template>
    <div
      v-for="comment in comments"
      :key="comment.created"
      class="mb-4"
    >
      <div class="flex items-center gap-2">
        <UserAvatar
          :user="comment.user"
          size="normal"
        />
        <span class="font-bold">{{ comment.user.full_name }}</span>
      </div>
      <blockquote>{{ comment.text }}</blockquote>
      <span class="text-xs text-slate-500">{{ d(comment.created, "long") }}</span>
      <Divider />
    </div>
    <form class="mt-8">
      <FloatLabel>
        <label for="post-comment">{{ t("comments.new_comment") }}</label>
        <Textarea
          id="post-comment"
          v-model="form.comment"
          class="w-full"
        />
      </FloatLabel>
      <Button
        class="w-full mt-2"
        :disabled="!form.comment.trim()"
        @click="postComment"
      >
        {{ t("comments.post") }}
      </Button>
    </form>
  </Panel>
</template>
