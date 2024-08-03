import { createI18n } from 'petite-vue-i18n'

import { languages, defaultLocale } from "../i18n";
const messages = Object.assign(languages);

export const i18n = createI18n({
  locale: defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
});
