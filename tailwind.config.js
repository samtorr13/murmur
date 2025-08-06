/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/templates/*.html'
    './static/**/*.js',
  ],
  theme: {
    extend: {
      // Aquí puedes extender colores, fuentes, etc.
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake", "forest", "aqua", "lofi"], // o los que quieras
  },
};