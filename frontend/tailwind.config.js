/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#6C5CE7', // Vibrant Purple
                secondary: '#00CEC9', // Teal
                accent: '#FD79A8', // Pink
                surface: '#F8F9FA', // Light Gray/White
                dark: '#2D3436', // Dark Gray
                card: '#FFFFFF',
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
