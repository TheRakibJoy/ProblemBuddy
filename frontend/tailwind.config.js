/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{ts,tsx}", "../templates/**/*.html"],
  darkMode: ['class', '[data-bs-theme="dark"]'],
  corePlugins: {
    // Tailwind's `.collapse` utility (visibility: collapse) conflicts with
    // Bootstrap's `.collapse` class used for expandable navbar/accordion.
    visibility: false,
  },
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: "#3b82f6",
          foreground: "#ffffff",
        },
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "-400px 0" },
          "100%": { backgroundPosition: "400px 0" },
        },
      },
      animation: {
        shimmer: "shimmer 1.2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
