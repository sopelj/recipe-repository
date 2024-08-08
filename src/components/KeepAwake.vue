<script setup lang="ts">
import { ref } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const supported = ref<boolean>("wakeLock" in navigator);
const wakeLock = ref<WakeLockSentinel>();

const handleRelease = () => {
  wakeLock.value = undefined;
};

const toggleWakeLock = async () => {
  if (!wakeLock.value) {
    const lock = await navigator.wakeLock.request("screen");
    lock.addEventListener("release", handleRelease);
    wakeLock.value = lock;
  } else {
    await wakeLock.value?.release();
    wakeLock.value?.removeEventListener("release", handleRelease);
    wakeLock.value = undefined;
  }
};
</script>

<template>
  <label class="flex items-center">
    {{ t("global.keep_screen_on") }}
    <ToggleSwitch
      :model-value="!!wakeLock"
      :disabled="!supported"
      class="ml-1"
      @change="toggleWakeLock"
    />
  </label>
</template>
