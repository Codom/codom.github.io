<script>
import WelcomeItem from './WelcomeItem.vue'
</script>

<template>
  <WelcomeItem>
    <template #heading>Blog</template>

    <h2>
        <router-link to="/blog/vue_port">
            Porting site to vue - 11/16/2023
        </router-link>
    </h2>
    <h2><router-link to="/blog/static_website">Overhaul of static website generation - 09/28/2022</router-link></h2>
  </WelcomeItem>
</template>
