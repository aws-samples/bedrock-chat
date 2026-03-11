/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    fontFamily: {
      body: ['Arial Narrow', 'Arial', 'sans-serif'],
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
        'aws-squid-ink': {
          light: '#6C3F99',
          dark: '#171717',
        },
        'aws-sea-blue': {
          light: '#005276',
          dark: '#757575',
        },
        'aws-sea-blue-hover': {
          light: '#003550',
          dark: '#5b5b5b',
        },
        'aws-aqua': '#007faa',
        'aws-lab': '#38ef7d',
        'aws-mist': '#9ffcea',
        'aws-font-color': {
          light: '#232F3E',
          dark: '#cacaca',
          gray: '#909193',
          blue: '#276cc6',
        },
        'aws-font-color-white': {
          light: '#ffffff',
          dark':'#ececec',
        },
        'aws-ui-color': {
          dark: '#151515',
        },
        'aws-paper': {
          light: '#f1f3f3',
          dark: '#212121',
        },
        'aws-sidebar': {
          light: '#5a3380',
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
