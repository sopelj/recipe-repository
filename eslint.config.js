 //@ts-check
 import eslint from "@eslint/js";
 import tseslint from "typescript-eslint";
 import pluginVue from "eslint-plugin-vue";
 import eslintConfigPrettier from "eslint-config-prettier";

 export default tseslint.config(
   {ignores: ["**/*.js"]},
   eslint.configs.recommended,
   ...tseslint.configs.recommended,
   ...pluginVue.configs['flat/recommended'],
   {
     ignores: ["**/*.js"],
     plugins: {
       'typescript-eslint': tseslint.plugin,
     },
     languageOptions: {
       parserOptions: {
         parser: tseslint.parser,
         project: "./tsconfig.json",
         extraFileExtensions: [".vue"],
         sourceType: 'module',
       },
     },
   },
   eslintConfigPrettier,
 );
