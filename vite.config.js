import { fileURLToPath, URL } from 'node:url'
import fs from 'fs'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Read blog posts for SSG
const getBlogRoutes = () => {
  try {
    const data = fs.readFileSync('./src/data/blog/index.json', 'utf8')
    const posts = JSON.parse(data)
    return posts.map(post => post.path)
  } catch (e) {
    console.warn('Could not read blog index:', e.message)
    return []
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  ssgOptions: {
    script: 'async',
    formatting: 'minify',
    includedRoutes(paths) {
      // Include all static routes
      const staticRoutes = paths.filter(path => !path.includes(':'))
      // Add dynamic blog routes
      const blogRoutes = getBlogRoutes()
      return [...staticRoutes, ...blogRoutes]
    }
  }
})
