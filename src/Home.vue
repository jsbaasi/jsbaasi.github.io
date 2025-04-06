<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <div class="min-h-screen flex bg-[#222034] text-[#f0e6d2] font-['Press_Start_2P']">
    
    <!-- Left Section -->
    <div class="w-1/2 flex flex-col justify-center items-start px-20 space-y-8">
      <h1 class="text-3xl tracking-widest text-[#f0e6d2]">jsbaasi</h1>

      <button class="px-6 py-3 bg-[#c9a066] hover:bg-[#b88e55] text-[#2e1e0f] border-2 border-[#8b5a2b] text-sm uppercase tracking-wide">
        Projects
      </button>

      <button class="px-6 py-3 bg-[#c9a066] hover:bg-[#b88e55] text-[#2e1e0f] border-2 border-[#8b5a2b] text-sm uppercase tracking-wide">
        What I'm Reading
      </button>
    </div>

    <!-- Right Section (Campfire GIF) -->
    <div class="w-1/2 flex items-center justify-center bg-[#222034] border-l-2 border-[#222034]/30">
      <!-- Add the GIF here, with controlled size -->
      <img src="/campfire.gif" alt="Campfire" class="w-19/20 h-auto" />
    </div>

  </div>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>