<script setup lang="ts">
import type { Comment } from "@/types/recipes";

import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import UserAvatar from "@/components/UserAvatar.vue";

defineProps<{ comments: Comment[] }>();

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
  <div>
    <h3>{{ t("comments.title") }}</h3>
    <Panel
      v-for="comment in comments"
      :key="comment.created"
      class="mb-4"
    >
      <template #header>
        <div class="flex items-center gap-2">
          <UserAvatar
            :user="comment.user"
            size="normal"
          />
          <span class="font-bold">{{ comment.user.full_name }}</span>
        </div>
      </template>
      <blockquote>{{ comment.text }}</blockquote>
      <template #footer>
        <span class="text-xs text-slate-500">{{ d(comment.created, "long") }}</span>
      </template>
    </Panel>
    <Card>
      <template #content>
        <FloatLabel>
          <label for="post-comment">{{ t("comments.new_comment") }}</label>
          <Textarea
            id="post-comment"
            v-model="form.comment"
            class="w-full"
          />
        </FloatLabel>
      </template>
      <template #footer>
        <Button
          class="w-full"
          :disabled="!form.comment.trim()"
          @click="postComment"
        >
          {{ t("comments.post") }}
        </Button>
      </template>
    </Card>
  </div>
</template>
