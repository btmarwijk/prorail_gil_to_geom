import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // This maps '@' to your 'src' folder
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true, // Also fixes the binding issue above
    port: 5173,
    watch: {
      usePolling: true, // Often needed for Podman/Docker volumes on Windows/Mac
    },
    hmr: {
      clientPort: 5173 // Forces WebSocket to use the exposed port
    },
  proxy: {
  '/geoserver': {
    target: 'http://geoserver:8080', // GeoServer container hostname
    changeOrigin: true,
    rewrite: (path) => path, // Keep the path as-is
  },
},
  }
})
