<template>
    <div class="post">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-if="error" class="error">{{ error }}</div>

        <div v-if="post" class="content">
            <div v-html="post" class="content"></div>
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
.post {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  color: #2c3e50;
}

.loading, .error {
  text-align: center;
  font-size: 1.2rem;
  padding: 2rem;
}

.error {
  color: #e74c3c;
}

/* Markdown Content Styles */
.content {
  line-height: 1.8;
  font-size: 1.1rem;
}

.content h1, .content h2, .content h3, .content h4 {
  color: #2c3e50;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.content h1 { font-size: 2.2rem; border-bottom: 2px solid #eaeaea; padding-bottom: 0.5rem; }
.content h2 { font-size: 1.8rem; }
.content h3 { font-size: 1.5rem; }

.content p {
  margin-bottom: 1.5rem;
}

.content a {
  color: #42b883;
  text-decoration: none;
  border-bottom: 1px dotted #42b883;
}

.content a:hover {
  border-bottom-style: solid;
}

.content ul, .content ol {
  margin-bottom: 1.5rem;
  padding-left: 2rem;
}

.content li {
  margin-bottom: 0.5rem;
}

.content pre {
  background: #f8f8f8;
  padding: 1.5rem;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 1.5rem;
  border: 1px solid #eaeaea;
}

.content code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  background: #f0f0f0;
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
  background: #f9f9f9;
  font-style: italic;
  color: #555;
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
