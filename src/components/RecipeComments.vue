<script setup lang="ts">
import type { Comment } from "@/types/recipes";

import { useForm } from "@inertiajs/vue3";
import { useI18n } from "vue-i18n";

import { formatTimeSince } from "@/utils/durations";

import CollapsibleItem from "@/components/CollapsibleItem.vue";
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
  <collapsible-item>
    <template #title>
      <h3>
        {{ t("comments.title") }}
        <span
          v-if="comments.length"
          class="badge badge-primary"
        >
          {{ comments.length }}
        </span>
      </h3>
    </template>
    <template #content>
      <div
        v-for="comment in comments"
        :key="comment.created"
        class="p-2 mb-2 flex body-content"
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
    </template>
  </collapsible-item>
</template>
