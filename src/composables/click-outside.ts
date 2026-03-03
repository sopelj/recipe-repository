import { onMounted, onUnmounted, Ref } from "vue";

export const useClickOutside = (elRef: Ref<HTMLElement | undefined>, callback: () => void) => {
  const handleClickOutside = (event: MouseEvent) => {
    if (!elRef.value?.contains(event.target as Node)) {
      callback();
    }
  };
  onMounted(() => {
    document.addEventListener("click", handleClickOutside);
  });
  onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside);
  });
};
