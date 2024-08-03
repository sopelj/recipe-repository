// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-plugin-prettier/recommended";

export default tseslint.config(
    {
        files: ["**/*.vue", "**/*.js", "**/*.ts"],
        ignores: ["./static/**"],
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
            parserOptions: {
                parser: tseslint.parser,
                project: "./tsconfig.json",
                extraFileExtensions: [".vue"],
                sourceType: "module",
            },
        },
        rules: {
            "vue/component-api-style": ["error", ["script-setup"]],
            "vue/component-name-in-template-casing": "error",
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
        },
    },
    prettier,
    {
        rules: {
            "prettier/prettier": "warn",
        },
    },
);
