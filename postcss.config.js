/** @type {import('postcss-load-config').Config} */
export default {
  plugins: {
    "@tailwindcss/postcss": {},
    "autoprefixer": {},
    ...(import.meta.PROD ? { cssnano: {} } : {}),
  },
};
