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
        },
        bluesea: {
          50: '#e8f8fc',
          100: '#d1f1f9',
          200: '#a3e3f3',
          300: '#75d5ed',
          400: '#50d4e8',
          500: '#22bfda',
          600: '#1a99b0',
          700: '#137387',
          800: '#0d4d5d',
          900: '#1e4a6f'
        }
      }
    }
  },
  plugins: []
};
