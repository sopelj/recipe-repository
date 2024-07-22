import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";

import PrimeVue from "primevue/config";
import Tooltip from 'primevue/tooltip';
import Aura from "@primevue/themes/aura";
import MainLayout from "./layouts/MainLayout.vue";

import "./style.scss";


await createInertiaApp({
  resolve: name => {
    const pages = import.meta.glob('./pages/**/*.vue', { eager: true });
    const page = pages[`./pages/${name}.vue`];
    page.default.layout = page.default.layout || MainLayout;
    return page;
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) });
    app.use(plugin);
    app.use(PrimeVue, {
      theme: {
        preset: Aura,
        options: {
          cssLayer: {
            name: 'primevue',
            order: 'tailwind-base, primevue, tailwind-utilities'
          }
        }
      }
    });

    app.directive('tooltip', Tooltip);
    app.mount(el);
  },
})
