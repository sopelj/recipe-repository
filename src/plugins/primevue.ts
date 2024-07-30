import type { App } from "vue";

import PrimeVue from "primevue/config";
import Tooltip from 'primevue/tooltip';

import Aura from '@primevue/themes/aura';
import { definePreset } from "@primevue/themes";

const SiteTheme = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{purple.50}',
            100: '{purple.100}',
            200: '{purple.200}',
            300: '{purple.300}',
            400: '{purple.400}',
            500: '{purple.500}',
            600: '{purple.600}',
            700: '{purple.700}',
            800: '{purple.800}',
            900: '{purple.900}',
            950: '{purple.950}'
        }
    }
});

export const setupPrimeVue = (app: App) => {
    app.use(PrimeVue, {
        theme: {
        preset: SiteTheme,
        options: {
            cssLayer: {
                name: 'primevue',
                order: 'tailwind-base, primevue, tailwind-utilities'
            }
        }
    }
    });

    // Directives
    app.directive('tooltip', Tooltip);
};
