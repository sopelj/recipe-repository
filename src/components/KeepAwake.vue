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
  <div class="flex items-center gap-1">
    <input
      id="screen-wake-switch"
      :disabled="!supported"
      :value="!!wakeLock"
      type="checkbox"
      class="switch border-purple-700 bg-purple-500/20 switch-primary"
      @change="toggleWakeLock"
    />
    <label
      class="label-text text-base"
      for="screen-wake-switch"
    >
      {{ t("global.keep_screen_on") }}
    </label>
  </div>
</template>
