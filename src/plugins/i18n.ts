import { createI18n } from "vue-i18n";

import { messages, defaultLocale } from "../i18n";

export const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
});
