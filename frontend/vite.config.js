import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    allowedHosts: true,
    proxy: {
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/projects': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/generate': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/refine': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/feedback': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/comments': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/sections': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/export': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ai': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
