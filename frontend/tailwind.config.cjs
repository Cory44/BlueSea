module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ocean: {
          50: '#f2f8ff',
          100: '#dceeff',
          200: '#b8dcff',
          300: '#8ac3ff',
          400: '#5aa6ff',
          500: '#2b84ff',
          600: '#0b62db',
          700: '#034cb0',
          800: '#063d88',
          900: '#092f66'
        }
      }
    }
  },
  plugins: []
};
