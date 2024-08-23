// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ["@/assets/style/main.scss"],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "@/assets/style/_variables.scss";@import "@/assets/style/_icons.scss";',
        },
      },
    },
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:5001',  // FlaskサーバーのURL
          changeOrigin: true,                // オリジンを変更
          rewrite: (path) => path.replace(/^\/api/, ''),  // `/api`を削除してFlaskにリクエストを転送
        }
      }
    }
  },
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true }
})