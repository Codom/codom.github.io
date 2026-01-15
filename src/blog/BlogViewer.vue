<template>
    <div class="page-wrapper">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <div v-if="post" class="paper-card">
            <div v-html="post" class="content markdown-body"></div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loading: false,
            post: null,
            error: null,
        }
    },    // watch the params of the route to fetch the data again
    created() {
        this.$watch(
          () => this.$route.params,
          () => {
            this.fetchData()
          },
          // fetch the data when the view is created and the data is
          // already being observed
          { immediate: true }
        )
    },
    methods: {
        fetchData() {
          this.error = this.post = null
          this.loading = true
          const data_uri = this.$route.params.id + '.html'
          fetch(data_uri).then(async (response) => {
            this.loading = false
            if (!response.ok) {
              this.error = await response.error()
            } else {
              const html_text = await response.text()
              this.post = html_text
            }
          })
        },
    },
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
