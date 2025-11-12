import type { App } from "vue";

import Aura from "@primeuix/themes/aura";
import { definePreset } from "@primevue/themes";

import PrimeVue from "primevue/config";
import ToastService from "primevue/toastservice";
import Tooltip from "primevue/tooltip";

const SiteTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50: "{purple.50}",
      100: "{purple.100}",
      200: "{purple.200}",
      300: "{purple.300}",
      400: "{purple.400}",
      500: "{purple.500}",
      600: "{purple.600}",
      700: "{purple.700}",
      800: "{purple.800}",
      900: "{purple.900}",
      950: "{purple.950}",
    },
  },
});

export const setupPrimeVue = (app: App) => {
  app.use(PrimeVue, {
    theme: {
      preset: SiteTheme,
      options: {
        cssLayer: {
          name: "primevue",
          order: "theme, base, primevue",
        },
      },
    },
  });

  // Directives
  app.directive("tooltip", Tooltip);

  // Toasts
  app.use(ToastService);
};
