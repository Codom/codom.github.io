<template>
    <div class="page-wrapper">
        <div class="paper-card">
            <div v-html="postContent" class="content markdown-body"></div>
        </div>
    </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import simpleGuitarAmp from '../../public/blog/simple_guitar_amp.html?raw'
import vuePort from '../../public/blog/vue_port.html?raw'
import staticWebsite from '../../public/blog/static_website.html?raw'

const posts = {
    'simple_guitar_amp': simpleGuitarAmp,
    'vue_port': vuePort,
    'static_website': staticWebsite
}

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
<style>
/* Additional specific styles for blog content that might not be in global markdown-body */
.content pre {
  background: #f8f8f8;
  padding: 1.5rem;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  border: 1px solid var(--color-border);
}

.content code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  background: var(--color-background-mute);
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.9em;
  color: #e01b24;
}

.content pre code {
  background: transparent;
  padding: 0;
  color: #333;
  border: none;
}

.content blockquote {
  border-left: 4px solid #42b883;
  margin: 1.5rem 0;
  padding: 0.5rem 1rem;
  background: var(--color-background-mute);
  font-style: italic;
  color: var(--color-text);
}

.content img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
  display: block;
  margin: 2rem auto;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
