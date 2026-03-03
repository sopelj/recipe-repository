/** @type {import('postcss-load-config').Config} */
export default {
  plugins: {
    "autoprefixer": {},
    ...(import.meta.PROD ? { cssnano: {} } : {}),
  },
};
