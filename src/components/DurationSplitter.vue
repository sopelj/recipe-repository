<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { formatDuration } from "@/utils/durations";

const props = defineProps<{ type: string; time?: string }>();
const { t } = useI18n();

const formattedDuration = computed((): string => (props?.time ? formatDuration(props.time) : ""));
const isoTime = computed((): string => `PT${formattedDuration.value.replace(" ", "").toUpperCase()}`);
</script>

<template>
  <splitter-panel
    v-if="time"
    class="flex items-center justify-center m-2"
  >
    {{ t(`times.${type}`) }}&nbsp;<meta
      :itemprop="`${type}Time`"
      :content="isoTime"
    />{{ formattedDuration }}
  </splitter-panel>
</template>
