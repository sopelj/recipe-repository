/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_APP_TITLE_SHORT: string;
  readonly VITE_APP_THEME_COLOUR: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
