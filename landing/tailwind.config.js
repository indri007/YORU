/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        yoru: {
          bg: "#0E0F14",
          surface: "#14161F",
          card: "#191C27",
          border: "rgba(232, 182, 76, 0.15)",
          gold: "#E8B64C",
          "gold-light": "#F7D58B",
          "gold-glow": "rgba(232, 182, 76, 0.35)",
          cream: "#F2EFE6",
          muted: "#9E9AA7",
          night: "#1E2235",
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
      animation: {
        'float-slow': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 3s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        pulseGlow: {
          '0%': { opacity: '0.4', filter: 'blur(10px)' },
          '100%': { opacity: '0.8', filter: 'blur(16px)' },
        }
      }
    },
  },
  plugins: [],
}
