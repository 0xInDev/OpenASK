// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  css: [
    'vuetify/lib/styles/main.sass', 
    '@mdi/font/css/materialdesignicons.min.css'
 ],
  build: {
    transpile: ['vuetify'],
  },
  vite: {
    define: {
      'process.env.DEBUG': false,
    },
  },
  runtimeConfig: {
    public: {
      API_URL: 'http://127.0.0.1:8000'
    }
  },
})
