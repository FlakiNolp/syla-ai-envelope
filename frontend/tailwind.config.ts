import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary-color)",
        secondary: "var(--secondary-color)",
        tertiary: "var(--tertiary-color)",
      },
      fontFamily: {
        saar: ["var(--font-saar)"],
        instrumentSans: ["var(--font-instrument-sans)"],
      }
    },
  },
  plugins: [],
};
export default config;
