/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'smk-blue': '#1e3a8a',
        'smk-light-blue': '#3b82f6',
        'smk-gray': '#6b7280',
        'smk-light-gray': '#f3f4f6',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

