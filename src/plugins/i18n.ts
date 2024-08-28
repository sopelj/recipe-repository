import messages from "@intlify/unplugin-vue-i18n/messages";
import { createI18n, type DefineDateTimeFormat } from "vue-i18n";

const currentLocale = window.location.pathname.split("/")[1];

const baseDateConfig: DefineDateTimeFormat = {
  short: {
    year: "numeric",
    month: "short",
    day: "numeric",
  },
  long: {
    year: "numeric",
    month: "short",
    day: "numeric",
    weekday: "short",
    hour: "numeric",
    minute: "numeric",
  },
};

const datetimeFormats = {
  "en": baseDateConfig,
  "fr": baseDateConfig,
  "ja": baseDateConfig,
};

export const i18n = createI18n({
  legacy: false,
  locale: currentLocale || "en",
  fallbackLocale: "en",
  messages,
  datetimeFormats,
});
