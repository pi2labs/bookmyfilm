<script setup>
import Navbar from './components/layout-component/navbar/Navbar.vue'
</script>

<template>
  <div
    class="min-h-screen text-slate-100 bg-gradient-to-b from-[#060a12] via-[#0b1220] to-[#060a12]"
  >
    <Navbar />
    <main class="pt-3 sm:pt-4">
      <router-view />
    </main>
  </div>
</template>