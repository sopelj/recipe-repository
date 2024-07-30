export default {
    darkMode: ['selector', '[class*="app-dark"]'],
    content: ['./index.html', './src/**/*.{vue,js,ts}'],
    plugins: [require('tailwindcss-primeui')],
};
