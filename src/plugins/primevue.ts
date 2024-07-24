import type { App } from "vue";

import PrimeVue from "primevue/config";
import Tooltip from 'primevue/tooltip';

// @ts-expect-error presets do not yet support TypeScript
import Aura from "./presets/aura";

export const setupPrimeVue = (app: App) => {
    app.use(PrimeVue, {
        unstyled: true,
        pt: Aura,
        darkMode: 'class',
    });

    // Directives
    app.directive('tooltip', Tooltip);
};
