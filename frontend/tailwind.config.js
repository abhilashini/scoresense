/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // This tells Tailwind to look in all .html and all .jsx files in the src directory
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}