<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { computed } from "vue";
import { formatLocalised, formatISOTime } from "@/utils/durations";

const types = ["prepTime", "cookTime", "totalTime"] as const;
type DurationType = typeof types[number];
type Duration = { time: string, type: DurationType};

const props = defineProps<{ prepTime?: string; cookTime?: string; totalTime?: string }>();

const { t } = useI18n();
const durations = computed(
  () => types.reduce((acc: Duration[], type: DurationType) => {
    const time = props[type];
    if (time) {
      acc.push({ type, time })
    }
    return acc;
  }, [])
);
</script>

<template>
  <Splitter v-if="totalTime">
    <SplitterPanel
      v-for="duration in durations"
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
