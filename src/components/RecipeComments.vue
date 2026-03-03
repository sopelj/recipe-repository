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
  <div class="card">
    <div class="card-title">
      <h3>
        {{ t("comments.title") }}
        <span
          v-if="comments.length"
          class="badge badge-primary"
        >
          {{ comments.length }}
        </span>
      </h3>
    </div>
    <div
      v-for="comment in comments"
      :key="comment.created"
      class="my-2 flex body-content"
    >
      <div class="mr-1">
        <user-avatar
          :user="comment.user"
          size="sm"
        />
      </div>
      <div class="grow">
        <blockquote style="white-space: pre">{{ comment.text }}</blockquote>
        <span class="text-xs text-slate-500">{{ formatTimeSince(comment.created) }}</span>
        <div class="divider"></div>
      </div>
    </div>
    <form class="mt-2 card border rounded-sm p-2">
      <label for="post-comment">{{ t("comments.new_comment") }}</label>
      <textarea
        id="post-comment"
        v-model="form.comment"
        class="w-full mt-1"
      />
      <button
        class="w-full mt-2 btn"
        :disabled="!form.comment.trim()"
        @click="postComment"
      >
        {{ t("comments.post") }}
      </button>
    </form>
  </div>
</template>
