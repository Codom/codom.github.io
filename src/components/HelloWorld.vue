<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
        <p>Software Engineer</p>
        <router-link to="/">Home</router-link> |
        <router-link to="/Blog">Blog</router-link> |
        <a href='/resume.pdf'>Resume</a> |
        <a href='https://github.com/Codom'>Github</a>
    </h3>
  </div>
</template>

<style scoped>

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

</style>
