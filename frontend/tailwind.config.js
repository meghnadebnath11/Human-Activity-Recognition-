/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#07111f",
        sunrise: "#f97316",
        sand: "#f5e9d7",
        ocean: "#0f766e",
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        body: ["Trebuchet MS", "sans-serif"],
      },
      boxShadow: {
        panel: "0 20px 45px rgba(2, 6, 23, 0.18)",
      },
    },
  },
  plugins: [],
};

