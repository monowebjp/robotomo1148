// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ["@/assets/style/main.scss"],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "@/assets/style/_variables.scss";',
        },
      },
    },
  },
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true }
})
