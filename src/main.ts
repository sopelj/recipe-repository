import { createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";
import "./style.css";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import "primeicons/primeicons.css";
import MainLayout from "./layouts/MainLayout.vue";


createInertiaApp({
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
    app.mount(el);
  },
})
