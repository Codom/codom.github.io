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
        <nav>
            <router-link to="/">Home</router-link>
            <router-link to="/blog">Projects</router-link>
            <router-link to="/resume">Resume</router-link>
            <a href='https://github.com/Codom' target="_blank">Github</a>
        </nav>
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

nav {
  margin-top: 10px;
}

nav a {
  margin: 0 10px;
  text-decoration: none;
  color: var(--color-text);
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

nav a.router-link-active {
    color: #42b883; /* Vue green */
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

</style>
