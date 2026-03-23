/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    fontFamily: {
      body: ['Open Sans', 'sans-serif'],
      heading: ['Yu Gothic Medium', 'Yu Gothic', 'sans-serif'],
    },
    extend: {
      transitionProperty: {
        width: 'width',
        height: 'height',
      },
      animation: {
        fastPulse: 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 1.8s linear infinite',
        'typing-dot-1': 'typingDot 1.4s ease-in-out 0s infinite',
        'typing-dot-2': 'typingDot 1.4s ease-in-out 0.2s infinite',
        'typing-dot-3': 'typingDot 1.4s ease-in-out 0.4s infinite',
        'fade-in': 'fadeIn 0.25s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
        typingDot: {
          '0%, 60%, 100%': { opacity: '0.15', transform: 'translateY(0)' },
          '30%': { opacity: '1', transform: 'translateY(-4px)' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      colors: {
        // ACIL Allen brand colour palette
        // Colour hierarchy: Purple → Grey → Blue → Green
        'aa-purple': {
          1: '#140034',
          2: '#331063',
          3: '#6C3F99',
          4: '#9D85BE',
          5: '#CCC3DC',
        },
        'aa-grey': {
          1: '#000000',
          2: '#4D4D4D',
          3: '#7D7D7D',
          4: '#C8C8C8',
          5: '#E5E5E5',
        },
        'aa-blue': {
          1: '#001E32',
          2: '#00486E',
          3: '#006A9F',
          4: '#7BBDD6',
          5: '#C4DDE9',
        },
        'aa-green': {
          1: '#102515',
          2: '#004016',
          3: '#428D52',
          4: '#9FD18B',
          5: '#D4E7C8',
        },
        // Semantic UI tokens mapped to ACIL Allen brand colours
        'aws-squid-ink': {
          light: '#6C3F99', // AA Purple 3 — primary brand purple
          dark: '#171717',
        },
        'aws-sea-blue': {
          light: '#006A9F', // AA Blue 3
          dark: '#757575',
        },
        'aws-sea-blue-hover': {
          light: '#00486E', // AA Blue 2
          dark: '#5b5b5b',
        },
        'aws-aqua': '#7BBDD6', // AA Blue 4
        'aws-lab': '#9FD18B',  // AA Green 4
        'aws-mist': '#D4E7C8', // AA Green 5
        'aws-font-color': {
          light: '#4D4D4D', // AA Grey 2
          dark: '#cacaca',
          gray: '#7D7D7D',  // AA Grey 3
          blue: '#006A9F',  // AA Blue 3
        },
        'aws-font-color-white': {
          light: '#ffffff',
          dark: '#ececec',
        },
        'aws-ui-color': {
          dark: '#151515',
        },
        'aws-paper': {
          light: '#f1f3f3',
          dark: '#212121',
        },
        'aws-sidebar': {
          light: '#331063', // AA Purple 2
          dark: '#111111',
        },
        red: '#dc2626',
        'light-red': '#fee2e2',
        yellow: '#f59e0b',
        'light-yellow': '#fef9c3',
        'dark-gray': '#6b7280',
        gray: '#9ca3af',
        'light-gray': '#e5e7eb',
      },
    },
  },
  // eslint-disable-next-line no-undef
  plugins: [require('@tailwindcss/typography'), require('tailwind-scrollbar')],
};
