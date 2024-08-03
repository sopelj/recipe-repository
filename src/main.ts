import { type ComponentInstance, type Component, createApp, h } from "vue";
import { createInertiaApp } from "@inertiajs/vue3";

import { setupPrimeVue } from "./plugins/primevue";
import { i18n } from "./plugins/i18n";

import MainLayout from "./layouts/MainLayout.vue";

import "./style.scss";

await createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob<ComponentInstance<Component>>("./pages/**/*.vue", { eager: true });
    const page = pages[`./pages/${name}.vue`];
    page.default.layout = page.default.layout || MainLayout;
    return page;
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) });
    app.use(i18n);
    app.use(plugin);
    setupPrimeVue(app);
    app.mount(el);
  },
});
