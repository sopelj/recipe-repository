import { createI18n } from "vue-i18n";

import { messages, defaultLocale } from "../i18n";

const currentLocale = window.location.pathname.split("/")[1];

export const i18n = createI18n({
  legacy: false,
  locale: currentLocale || defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
});
