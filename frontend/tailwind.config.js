/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        emergency: {
          critical: '#dc2626',
          high: '#ea580c',
          moderate: '#d97706',
          low: '#65a30d',
        },
        brand: {
          50: '#eff6ff',
          500: '#3b82f6',
          700: '#1d4ed8',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
