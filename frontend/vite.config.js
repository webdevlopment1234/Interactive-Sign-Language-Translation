import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const isProd = command === 'build';
  return {
    plugins: [react()],
    base: isProd ? '/static/' : '/',
    build: {
      outDir: 'dist',
      emptyOutDir: true
    },
    server: {
      proxy: {
        '/video_feed': 'http://127.0.0.1:5000',
        '/get_prediction': 'http://127.0.0.1:5000',
        '/api': 'http://127.0.0.1:5000',
        '/static': 'http://127.0.0.1:5000'
      }
    }
  };
})
