<template>
    <div class="post min-h-screen bg-[#fafafa] text-zinc-900">
        <div v-if="loading" class="text-zinc-500 py-12">Loading...</div>
        <div v-if="error" class="text-red-500 py-12">{{ error }}</div>

        <article v-if="post" class="max-w-3xl mx-auto px-6 py-16">
            <div v-html="post" class="prose prose-zinc prose-lg max-w-none"></div>
        </article>
    </div>
    <div class="page-wrapper">
        <div class="paper-card">
            <div v-html="postContent" class="content markdown-body"></div>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

// Dynamically import all blog HTML files at build time.
// Adding a new .md file in blog/ is all that's needed — build.py generates
// the HTML, and this glob picks it up automatically.
const rawPosts = import.meta.glob('../../public/blog/*.html', { as: 'raw', eager: true })

// Build a slug-keyed map: { 'vue_port': '<html>...' }
const posts = Object.fromEntries(
    Object.entries(rawPosts).map(([path, content]) => {
        const slug = path.split('/').pop().replace('.html', '')
        return [slug, content]
    })
)

export default {
    setup() {
        const route = useRoute()
        
        const postContent = computed(() => {
            return posts[route.params.id] || '<p>Post not found</p>'
        })
        
        return {
            postContent
        }
    }
}
</script>
<style scoped>
.prose {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.75;
}

.prose :deep(h1),
.prose :deep(h2),
.prose :deep(h3),
.prose :deep(h4) {
  font-weight: 600;
  color: #18181b;
  margin-top: 2em;
  margin-bottom: 0.75em;
  line-height: 1.3;
}

.prose :deep(h1) {
  font-size: 2rem;
}
.prose :deep(h2) {
  font-size: 1.5rem;
}
.prose :deep(h3) {
  font-size: 1.25rem;
}

.prose :deep(p) {
  margin-bottom: 1.5em;
  color: #52525b;
}

.prose :deep(a) {
  color: #18181b;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.prose :deep(a:hover) {
  color: #3b82f6;
}

.prose :deep(code) {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
  font-family: ui-monospace, monospace;
}

.prose :deep(pre) {
  background-color: #f4f4f5;
  border: 1px solid #e4e4e7;
  border-radius: 0.75rem;
  padding: 1.25rem;
  overflow-x: auto;
  margin: 1.5em 0;
}

.prose :deep(pre code) {
  background-color: transparent;
  padding: 0;
  font-size: 0.875em;
}

.prose :deep(ul),
.prose :deep(ol) {
  margin: 1em 0;
  padding-left: 1.5em;
  color: #52525b;
}

.prose :deep(li) {
  margin-bottom: 0.5em;
}

.prose :deep(blockquote) {
  border-left: 4px solid #e4e4e7;
  padding-left: 1em;
  margin: 1.5em 0;
  font-style: italic;
  color: #71717a;
}

.prose :deep(hr) {
  border: none;
  border-top: 1px solid #e4e4e7;
  margin: 2em 0;
}

.prose :deep(img) {
  max-width: 100%;
  border-radius: 0.5rem;
  margin: 1.5em 0;
}

.prose :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
}

.prose :deep(th),
.prose :deep(td) {
  border: 1px solid #e4e4e7;
  padding: 0.75rem;
  text-align: left;
}

.prose :deep(th) {
  background-color: #f4f4f5;
  font-weight: 600;
}
</style>
