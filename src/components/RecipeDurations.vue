<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import { formatISOTime, formatLocalised } from "@/utils/durations";

const props = defineProps<{ prepTime?: string; cookTime?: string; totalTime?: string }>();
const types = ["prepTime", "cookTime", "totalTime"] as const;
type DurationType = (typeof types)[number];
type Duration = { time: string; type: DurationType };

const { t } = useI18n();
const durations = computed(() =>
  types.reduce((acc: Duration[], type: DurationType) => {
    const time = props[type];
    if (time) {
      acc.push({ type, time });
    }
    return acc;
  }, []),
);
</script>

<template>
  <Splitter v-if="totalTime">
    <SplitterPanel
      v-for="duration in durations"
      :key="duration.type"
      :data-duration-type="duration.type"
      class="flex items-center justify-center m-2"
    >
      {{ t(`times.${duration.type}`, { duration: formatLocalised(duration.time) }) }}
      <meta
        :itemprop="duration.type"
        :content="formatISOTime(duration.time)"
      />
    </SplitterPanel>
  </Splitter>
</template>
