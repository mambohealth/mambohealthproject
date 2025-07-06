/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../../**/templates/**/*.html",  // All HTML templates across apps
    "../../templates/**/*.html",     // Global templates
    "../../**/*.py",                 // Optional: scan for class names in Python (StreamFields, etc.)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

