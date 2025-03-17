// @ts-check
import eslint from "@eslint/js";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import pluginVue from "eslint-plugin-vue";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    files: ["**/*.vue", "**/*.js", "**/*.ts"],
    ignores: ["./static/**"],
    plugins: { "simple-import-sort": simpleImportSort },
    rules: {
      "simple-import-sort/exports": "error",
      "quote-props": [2, "consistent-as-needed"],
      "prettier/prettier": "warn",
      "simple-import-sort/imports": [
        "error",
        {
          "groups": [
            // Type imports
            ["^[^\\.].+\\u0000$", "^.\\u0000$"],
            // @libraries
            ["^@", "^\\w+"],
            // Internal packages (@/, ../, ./)
            ["^@/", "^\\.\\.(?!/?$)", "^\\.\\./?$", "^\\./(?=.*/)(?!/?$)", "^\\.(?!/?$)", "^\\./?$"],
            // Components
            ["^primevue/.+", "\\.vue$"],
            // Style imports
            ["^.+\\.s?css$"],
            // Side effect imports
            ["^\\u0000"],
          ],
        },
      ],
    },
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs["flat/recommended"],
  {
    files: ["*.vue", "**/*.vue"],
    plugins: {
      "typescript-eslint": tseslint.plugin,
    },
    languageOptions: {
      globals: { ...globals.browser },
      parserOptions: {
        parser: tseslint.parser,
        project: "./tsconfig.json",
        extraFileExtensions: [".vue"],
        sourceType: "module",
      },
    },
    rules: {
      "vue/component-api-style": ["error", ["script-setup"]],
      "vue/define-props-declaration": "error",
      "vue/block-order": ["error", { order: ["script[setup]", "template", "style[scoped]"] }],
      "vue/block-lang": ["error", { script: { lang: "ts" } }],
      "vue/define-macros-order": [
        "error",
        {
          order: ["defineOptions", "defineModel", "defineProps", "defineEmits", "defineSlots"],
          defineExposeLast: true,
        },
      ],
      "vue/html-self-closing": ["error", { "html": { "void": "always" } }],
      "vue/singleline-html-element-content-newline": "off",
      // PascalCase is only used because PrimeVue and Inertia like use standard component names which conflict with real elements
      // And using PascalCase is essential to ensure these are correctly loaded.
      "vue/component-name-in-template-casing": [
        "error",
        "PascalCase",
        {
          "registeredComponentsOnly": false,
          globals: ["Button", "Image", "Menu", "Link"],
          ignores: ["Link"],
        },
      ],
    },
  },
  eslintPluginPrettierRecommended,
  {
    rules: {
      "prettier/prettier": "warn",
    },
  },
);
