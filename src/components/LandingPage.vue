<script setup>
import { 
  ArrowUpRight, 
  MapPin, 
  TerminalSquare, 
  Github, 
  Linkedin, 
  Mail,
  BookOpen,
  Coffee
} from 'lucide-vue-next';

const techStack = ['C/C++', 'FreeRTOS', 'Zephyr', 'ARM Cortex', 'U-Boot', 'Linux'];
</script>

<template>
  <div class="min-h-screen bg-[#fafafa] text-zinc-900 font-sans selection:bg-zinc-200">
    
    <!-- Minimalist Header -->
    <nav class="max-w-5xl mx-auto px-6 py-12 flex justify-between items-center">
      <div class="font-bold text-xl tracking-tight">Christopher Odom</div>
      <div class="flex items-center gap-4 text-sm font-medium text-zinc-500">
        <a href="#about" class="hover:text-zinc-900 transition-colors">About</a>
        <a href="#writings" class="hover:text-zinc-900 transition-colors">Writings</a>
        <a href="#contact" class="text-zinc-900 border-b border-zinc-900 pb-0.5">Contact</a>
      </div>
    </nav>

    <main class="max-w-5xl mx-auto px-6 pb-24">
      
      <!-- SECTION 1: The Clean Bento Grid (For scannable landing info) -->
      <section id="about" class="mb-24">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <!-- Main Intro Card -->
          <div class="md:col-span-2 md:row-span-2 bg-white rounded-3xl p-8 md:p-10 border border-zinc-200 shadow-sm flex flex-col justify-between">
            <div>
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-semibold tracking-wide uppercase mb-6">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Open to opportunities
              </div>
              <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-zinc-900 mb-4 leading-tight">
                Embedded systems engineer building <br class="hidden md:block"/> reliable firmware.
              </h1>
              <p class="text-lg text-zinc-500 max-w-lg leading-relaxed">
                Hi, I'm Christopher. I specialize in C/C++, RTOS, hardware integration, and creating robust software for resource-constrained devices.
              </p>
            </div>
            
            <div class="mt-8 flex items-center gap-4">
              <a href="/resume" class="bg-zinc-900 text-white px-6 py-3 rounded-full font-medium hover:bg-zinc-800 transition-colors flex items-center gap-2">
                View Resume <ArrowUpRight :size="18" />
              </a>
            </div>
          </div>

          <!-- Remote/Location Card -->
          <div class="bg-white rounded-3xl p-8 border border-zinc-200 shadow-sm flex flex-col justify-center relative overflow-hidden group">
            <MapPin :size="24" class="text-zinc-400 mb-4" />
            <h3 class="text-xl font-bold text-zinc-900 mb-1">100% Remote</h3>
            <p class="text-zinc-500 text-sm">Based in Boston, MA (EST). Seeking distributed team opportunities.</p>
            
            <!-- Decorative background element -->
            <div class="absolute -right-4 -bottom-4 opacity-5 group-hover:scale-110 transition-transform duration-500">
              <Coffee :size="100" stroke-width="1" />
            </div>
          </div>

          <!-- Tech Stack / Links Card -->
          <div class="bg-zinc-900 text-zinc-100 rounded-3xl p-8 shadow-sm flex flex-col justify-between">
            <div>
              <TerminalSquare :size="24" class="text-zinc-400 mb-4" />
              <h3 class="text-lg font-semibold mb-3">Core Focus</h3>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="tech in techStack" 
                  :key="tech" 
                  class="bg-zinc-800 text-zinc-300 border border-zinc-700 text-xs font-medium px-2.5 py-1 rounded-lg"
                >
                  {{ tech }}
                </span>
              </div>
            </div>
            <div class="flex gap-4 mt-6">
              <a href="https://github.com/Codom" class="text-zinc-400 hover:text-white transition-colors"><Github :size="20" /></a>
              <a href="https://www.linkedin.com/in/christopher-odom/" class="text-zinc-400 hover:text-white transition-colors"><Linkedin :size="20" /></a>
              <a href="mailto:christopher.r.odom@gmail.com" class="text-zinc-400 hover:text-white transition-colors"><Mail :size="20" /></a>
            </div>
          </div>

        </div>
      </section>

      <!-- SECTION 2: Minimalist Typography (For deep-dive content & writings) -->
      <section id="writings" class="mt-32">
        <div class="flex items-center gap-3 mb-12">
          <BookOpen :size="20" class="text-zinc-400" />
          <h2 class="text-sm font-bold tracking-widest uppercase text-zinc-500">Selected Writings</h2>
        </div>

        <div class="flex flex-col">
          <!-- Article 1 -->
          <a href="/blog/simple_guitar_amp" class="group py-8 border-t border-zinc-200 hover:bg-white hover:px-6 -mx-6 px-6 transition-all duration-300 rounded-2xl">
            <div class="flex flex-col md:flex-row md:items-baseline justify-between gap-2 mb-3">
              <h3 class="text-2xl md:text-3xl font-serif font-medium text-zinc-900 group-hover:text-blue-600 transition-colors">
                Building a guitar amp plugin in Zig with CLAP
              </h3>
              <span class="text-zinc-400 font-mono text-sm shrink-0">Jan 15, 2026</span>
            </div>
            <p class="text-zinc-500 text-lg max-w-3xl leading-relaxed">
              A deep dive into building a DSP audio plugin from scratch. Covering the signal chain, biquad filters, and synchronizing parameters between the audio and main threads.
            </p>
          </a>

          <!-- Article 2 -->
          <a href="/blog/vue_port" class="group py-8 border-t border-zinc-200 hover:bg-white hover:px-6 -mx-6 px-6 transition-all duration-300 rounded-2xl border-b">
            <div class="flex flex-col md:flex-row md:items-baseline justify-between gap-2 mb-3">
              <h3 class="text-2xl md:text-3xl font-serif font-medium text-zinc-900 group-hover:text-blue-600 transition-colors">
                Porting site to Vue
              </h3>
              <span class="text-zinc-400 font-mono text-sm shrink-0">Nov 16, 2023</span>
            </div>
            <p class="text-zinc-500 text-lg max-w-3xl leading-relaxed">
              I have spent the past few days porting my website into Vue. Documenting my learning process and integration with the existing build system.
            </p>
          </a>
        </div>

        <div class="mt-8">
          <a href="/blog" class="text-zinc-900 font-medium inline-flex items-center gap-2 hover:gap-3 transition-all border-b border-zinc-900 pb-0.5">
            View all writings <ArrowUpRight :size="16" />
          </a>
        </div>
      </section>

    </main>

    <!-- Minimal Footer -->
    <footer class="border-t border-zinc-200 bg-white">
      <div class="max-w-5xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-zinc-500">
        <p>© {{ new Date().getFullYear() }} Christopher Odom. All rights reserved.</p>
        <div class="flex gap-6">
          <a href="https://github.com/Codom" class="hover:text-zinc-900 transition-colors">GitHub</a>
          <a href="https://www.linkedin.com/in/christopher-odom/" class="hover:text-zinc-900 transition-colors">LinkedIn</a>
          <a href="mailto:christopher.r.odom@gmail.com" class="hover:text-zinc-900 transition-colors">Email</a>
        </div>
      </div>
    </footer>

  </div>
</template>
