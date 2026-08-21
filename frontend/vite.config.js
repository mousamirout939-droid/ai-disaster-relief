import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/api/v1/shelters/nearby'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'shelters-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 6 },
            },
          },
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/api/v1/incidents/nearby'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'incidents-cache',
              expiration: { maxEntries: 50, maxAgeSeconds: 60 * 30 },
            },
          },
        ],
      },
      manifest: {
        name: 'AI Disaster Relief & Rescue Platform',
        short_name: 'DisasterRelief',
        description: 'Real-time disaster reporting, shelter finding, and AI-guided emergency assistance.',
        theme_color: '#dc2626',
        background_color: '#0f172a',
        display: 'standalone',
        start_url: '/',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/ws': { target: 'ws://localhost:8000', ws: true },
    },
  },
})
