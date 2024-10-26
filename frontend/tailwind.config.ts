import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: "var(--primary)",
        secondary: "var(--secondary)",
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
