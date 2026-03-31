<script>
import WelcomeItem from './WelcomeItem.vue'
import postsData from '../data/blog/index.json'

export default {
  components: {
    WelcomeItem
  },
  setup() {
    return {
      posts: postsData
    }
  }
}
</script>

<template>
  <div class="page-wrapper">
      <div class="paper-card">
          <WelcomeItem>
            <template #heading>Projects</template>
            
            <div v-for="post in posts" :key="post.id" class="blog-entry">
                <h2>
                    <router-link :to="post.path">
                        {{ post.title }} - {{ post.date }}
                    </router-link>
                </h2>
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
