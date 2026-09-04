import type { Config } from "tailwindcss";

// Design tokens straight from the spec (section 7 — Color System).
// Never hardcode these hexes inside components; reference the Tailwind
// classes or CSS vars generated from this file instead.
const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        foreground: "var(--color-foreground)",
        navy: "var(--color-navy)",
        hero: "var(--color-hero)",
        mint: "var(--color-mint)",
        muted: "var(--color-muted)",
        border: "var(--color-border)",
      },
      fontFamily: {
        sans: ["var(--font-manrope)", "var(--font-inter)", "sans-serif"],
      },
      borderRadius: {
        panel: "1rem",
      },
    },
  },
  plugins: [],
};

export default config;
