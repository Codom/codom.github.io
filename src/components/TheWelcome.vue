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
    <template #heading>Skills</template>

    <h3>Software Engineering</h3>
    <div class="indented">
    <p>I started messing around in Python when I was in Middle School. Since then,
    I've honed my skills making software for fun and for work. While developing skills
    in C, C++, and Java, I learned the basics and started getting to work, picking up web
    development as I went along.</p>
    <p>Applying these skills in the field, as well
    as working on my own projects, is something that I deeply enjoy.</p>
    </div>

    <h3>Linux</h3>
    <div class="indented">
    <p>Once I graduated High School, I installed Linux on my laptop and never looked back.
    Since then, I've accrued 8 Years of experience in operating linux environments, ranging from
    personal computers to servers.</p>

    <p>In addition to running Linux as user, I also have practical experience using various syscall APIs
    directly.The most important ones being the socket API, inotify API (and by extension, poll and epoll),
    and libraries like io_uring.</p>
    </div>

    <h3>Low Level Graphics</h3>
    <div class="indented">
    <p>Mostly what I do whenever I'm programming for fun. I've written shaders, simple engines,
    and a lot of cool stuff in service of one day releasing a game.</p>
    </div>

    <h3>Security</h3>
    <div class="indented">
    <p>While not my main area of expertise, I was interested enough to participate in my University's
    CCDC team. I quickly learned the ropes on how to operate in a compromised Linux environment,
    and how to quickly bootstrap into a secure environment without loosing uptime.</p>
    </div>

    <h3>AI</h3>
    <div class="indented">
    <p>Most recent interest. I believe my skills in low-level graphics give me a very solid foundation
    to build out revolutionary new architectures for deep learning projects</p>
    </div>
  </WelcomeItem>

  <WelcomeItem>
    <template #heading>Featured Github Projects</template>
    <a href="https://github.com/Codom/SimpleGuitarAmp">Guitar Amp Simulator</a><br>
    <a href="https://github.com/Codom/Codom.github.io">Vue.js website</a><br>

  </WelcomeItem>
</template>

<style>
.indented {
  margin-left: 15px;
}
p {
  margin-bottom: 8px;
}
</style>
