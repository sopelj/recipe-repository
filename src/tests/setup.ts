import { config } from "@vue/test-utils";
import { createI18n } from "vue-i18n";
// import { vi } from 'vitest';

const i18n = createI18n({
  legacy: false,
  allowComposition: true,
});

config.global.plugins = [i18n];
