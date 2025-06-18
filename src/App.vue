<script setup>
import HelloWorld from './components/HelloWorld.vue'
import * as anim from './assets/animations.js'
</script>

<template>
  <header>
    <div class="wrapper">
      <HelloWorld msg="Christopher Odom" />
    </div>
  </header>

  <main>
     <router-view></router-view>
  </main>
  <div id = "animContainer"></div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

</style>
