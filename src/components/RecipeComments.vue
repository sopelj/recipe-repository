<script setup lang="ts">
import type { Comment } from "@/types/recipes";

import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import { formatTimeSince } from "@/utils/durations";

import UserAvatar from "@/components/UserAvatar.vue";

defineProps<{ comments: Comment[]; collapse?: boolean }>();

const { t } = useI18n();

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
      <Badge v-if="comments.length">{{ comments.length }}</Badge>
    </template>
    <div
      v-for="comment in comments"
      :key="comment.created"
      class="my-2 flex"
    >
      <UserAvatar
        v-tooltip="comment.user.full_name"
        :user="comment.user"
        size="large"
      />
      <div class="flex-grow">
        <blockquote style="white-space: pre">{{ comment.text }}</blockquote>
        <span class="text-xs text-slate-500">{{ formatTimeSince(comment.created) }}</span>
        <Divider />
      </div>
    </div>
    <form class="mt-2">
      <label for="post-comment">{{ t("comments.new_comment") }}</label>
      <Textarea
        id="post-comment"
        v-model="form.comment"
        class="w-full"
      />
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
