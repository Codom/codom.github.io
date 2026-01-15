<script>
import WelcomeItem from './WelcomeItem.vue'

export default {
  components: {
    WelcomeItem
  },
  data() {
    return {
      posts: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    fetch('/blog/index.json')
      .then(response => {
        if (!response.ok) throw new Error('Failed to load blog index')
        return response.json()
      })
      .then(data => {
        this.posts = data
        this.loading = false
      })
      .catch(err => {
        this.error = err.message
        this.loading = false
      })
  }
}
</script>

<template>
  <div class="page-wrapper">
      <div class="paper-card">
          <WelcomeItem>
            <template #heading>Blog</template>

            <div v-if="loading">Loading posts...</div>
            <div v-if="error">Error: {{ error }}</div>
            
            <div v-else>
                <div v-for="post in posts" :key="post.id" class="blog-entry">
                    <h2>
                        <router-link :to="post.path">
                            {{ post.title }} - {{ post.date }}
                        </router-link>
                    </h2>
                </div>
            </div>
          </WelcomeItem>
      </div>
  </div>
</template>

<style scoped>
.blog-entry {
    margin-bottom: 1rem;
}
</style>
