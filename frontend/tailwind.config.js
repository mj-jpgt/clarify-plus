/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary:   '#0b72ff',      // blue600
        accent:    '#ff9d00',      // orange500
        success:   '#009e9e',      // teal500
        danger:    '#ef4444',      // red500
        grayText:  '#4b5563',      // gray600
      },
      borderRadius: { 'xl2': '1.25rem' },
      boxShadow: { 'soft': '0 4px 14px rgba(0,0,0,.12)' },
    }
  },
  plugins: [],
}
