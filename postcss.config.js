/** @type {import('postcss-load-config').Config} */
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(import.meta.PROD ? { cssnano: {} } : {}),
  },
};
