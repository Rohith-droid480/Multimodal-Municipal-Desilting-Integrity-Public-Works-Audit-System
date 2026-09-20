import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./features/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        app: {
          bg: "#090D16",
          surface: "#0F172A",
          elevated: "#1E293B",
          active: "#334155",
          border: "#1E293B",
          "border-strong": "#334155",
          "border-focus": "#0EA5E9",
        },
        epistemic: {
          fact: "#0EA5E9",
          model: "#8B5CF6",
          rule: "#F59E0B",
          inference: "#3B82F6",
          recommendation: "#10B981",
        },
        severity: {
          critical: "#EF4444",
          high: "#F97316",
          medium: "#EAB308",
          inconclusive: "#64748B",
          clean: "#10B981",
        },
        canvas: {
          bg: "#FFFFFF",
          backdrop: "#F1F5F9",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
