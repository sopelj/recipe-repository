import { computed } from "vue";
type NavShare = Navigator & { share: (data: ShareData ) => Promise<void> };

export const useShare = () => {
  const canShare = computed(() => typeof window.navigator.share !== 'undefined');

  const share = async (title: string, text: string, url?: string) => {
    if (canShare.value) {
      await (navigator as NavShare).share({
        title,
        text,
        url: url || window.location.toString(),
      });
    }
  };
  return { canShare, share };
};
