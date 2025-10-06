module.exports = {
    darkMode: 'class',
    content: [
        './templates/**/*.html',
        './static/js/**/*.js'
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5f5',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a'
                }
            },
            fontFamily: {
                sans: ['IBM Plex Sans', 'Inter', 'system-ui', 'sans-serif']
            }
        }
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography')
    ]
};
