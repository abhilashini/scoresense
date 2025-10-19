import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: './',
  publicDir: 'public',
  build: {
    outDir: 'dist',
  },
  server: {
    port: 3000,
    open: true,
    // *** NEW PROXY CONFIGURATION ***
    proxy: {
      // Proxy requests starting with '/api' to the Flask server running on port 5000
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
    // *** END PROXY CONFIGURATION ***
  },
});