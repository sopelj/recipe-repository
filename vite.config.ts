import VueI18nPlugin from "@intlify/unplugin-vue-i18n/vite";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";
import VuePlugin from "@vitejs/plugin-vue";
import { fileURLToPath } from "node:url";
import { resolve } from "path";
import { visualizer } from "rollup-plugin-visualizer";
import Components from "unplugin-vue-components/vite";
import { defineConfig, loadEnv } from "vite";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [
      VuePlugin(),
      Components({ resolvers: [PrimeVueResolver()] }),
      VueI18nPlugin({ include: [resolve(__dirname, "./src/locales/**")] }),
      VitePWA({
        registerType: "autoUpdate",
        injectRegister: "auto",
        includeAssets: ["favicon.ico", "apple-touch-icon.png", "mask-icon.svg"],
        manifest: {
          name: env.VITE_APP_TITLE || "Recipe Repository",
          short_name: env.VITE_APP_TITLE_SHORT || "Recipes",
          description: env.VITE_APP_DESCRIPTION || "A repository for your favourite recipes.",
          theme_color: env.VITE_APP_THEME_COLOUR || "#482880",
          display: "standalone",
          start_url: "/",
          icons: [
            {
              src: "pwa-192x192.png",
              sizes: "192x192",
              type: "image/png",
            },
            {
              src: "pwa-512x512.png",
              sizes: "512x512",
              type: "image/png",
            },
          ],
        },
      }),
      visualizer(),
    ],
    root: resolve("./src"),
    base: "/static/",
    server: {
      host: true,
      port: 5173,
      open: false,
      watch: {
        usePolling: true,
        disableGlobbing: false,
      },
    },
    resolve: {
      extensions: [".vue", ".ts", ".js", ".json"],
      alias: [{ find: "@", replacement: fileURLToPath(new URL("./src", import.meta.url)) }],
    },
    build: {
      outDir: resolve("./dist"),
      manifest: "manifest.json",
      emptyOutDir: true,
      target: "es2022",
      rollupOptions: {
        input: {
          main: resolve("./src/main.ts"),
        },
        output: {
          chunkFileNames: undefined,
        },
      },
    },
    test: {
      globals: true,
      environment: "happy-dom",
      setupFiles: ["tests/setup.ts"],
    },
  };
});
