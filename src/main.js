import './assets/main.css'

import { ViteSSG } from 'vite-ssg'
import App from './App.vue'
import { routes } from './router'

// https://github.com/antfu/vite-ssg
export const createApp = ViteSSG(
  App,
  { routes },
  ({ app, router, routes, isClient, initialState }) => {
    // This runs on both server and client
  },
)
