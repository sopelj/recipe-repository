import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";
import Components from 'unplugin-vue-components/vite';
import { PrimeVueResolver } from '@primevue/auto-import-resolver';
import { fileURLToPath } from "node:url";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({ resolvers: [PrimeVueResolver()] }),
  ],
  root: resolve("./src"),
  base: "/static/",
  server: {
    host: "localhost",
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: [".vue", ".js", ".json"],
    alias: [
      { find: '@', replacement: fileURLToPath(new URL("./src", import.meta.url)) },
    ]
  },
  build: {
    outDir: resolve("./static/dist"),
    assetsDir: "",
    manifest: true,
    emptyOutDir: true,
    target: "es2020",
    rollupOptions: {
      input: {
        main: resolve("./src/main.tsx"),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
});