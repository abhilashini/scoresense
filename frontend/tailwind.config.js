/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Define a custom palette with a warm Gold/Saffron primary accent
      colors: {
        'primary': {
          50: '#FFFBEB',   // Very light background
          100: '#FEF3C7',
          400: '#FBBF24',
          500: '#F59E0B',  // Primary Gold/Saffron
          600: '#D97706',  // Deep Gold for buttons
          700: '#B45309',  // Darkest Gold for high contrast text
        },
        // Using a dark slate/charcoal for text and backgrounds
        'charcoal': '#1F2937', 
        'slate-light': '#4B5563',
      }
    },
  },
  plugins: [],
}