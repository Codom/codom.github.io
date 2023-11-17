<script setup>
import WelcomeItem from './WelcomeItem.vue'
</script>

<template>
  <WelcomeItem>
    <template #heading>About</template>

    I'm a software developer passionate about building
    the tech stack of the future. My main area of expertise
    is in low-level real-time sensitive software development,
    with projects in vst amp simulation, hobby gamedev,
    and professional experience in hardware testing tooling.
    In addition to this, I have a broader experience in
    web development including vuejs and rails, as well as
    general experience in securely deploying web services
    on aws and on bare metal.

  </WelcomeItem>

  <WelcomeItem>
    <template #heading>Featured Projects</template>
    <a href="https://github.com/Codom/Codom.github.io">Vue.js website</a>

  </WelcomeItem>
</template>
