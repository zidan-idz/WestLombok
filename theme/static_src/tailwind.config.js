/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '../../templates/**/*.html',
      '../../apps/**/*.py',
      '../../config/**/*.py',
  ],
  theme: {
    extend: {
      fontFamily: {
        'oswald': ['Oswald', 'sans-serif'],
        'roboto': ['Roboto', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        'placeholder': '#a8a8a8',
        'footer-gray': '#a8a8a8',
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
