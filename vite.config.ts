import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    cors: { origin: "*" },
  },
  base: '',
  root: 'frontend/',
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'frontend', 'index.html'),
        splash: resolve(__dirname, 'frontend', 'splash.html'),
        mainV2: resolve(__dirname, 'frontend', 'indexV2.html'),
        intro: resolve(__dirname, 'frontend', 'intro.html'),
        background: resolve(__dirname, 'frontend', 'background.html'),
      },
      output: {
        dir: "dist/",
      }
    },
  },
})
