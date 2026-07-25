/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brutalBg: '#f5f5f5',
        brutalBlue: '#0000ff',
        brutalYellow: '#ffff00',
        brutalGreen: '#00ff00',
        brutalRed: '#ff0000',
        brutalSecondary: '#6b7280',
      },
      boxShadow: {
        'brutal': '8px 8px 0px 0px rgba(0,0,0,1)',
      }
    },
  },
  plugins: [],
}