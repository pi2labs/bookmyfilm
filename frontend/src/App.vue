<script setup>
import { ref, provide, onMounted, watch } from 'vue'
import Navbar from './components/layout-component/navbar/Navbar.vue'
import CitySelectionModal from './components/CitySelectionModal.vue'

const isDarkMode = ref(false)

function toggleTheme() {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
  } else {
    // Default to light mode
    isDarkMode.value = false
  }
})

provide('theme', {
  isDarkMode,
  toggleTheme
})
</script>

<template>
  <div
    :class="[
      'min-h-screen transition-colors duration-300',
      isDarkMode 
        ? 'text-slate-100 bg-linear-to-b from-[#060a12] via-[#0b1220] to-[#060a12]'
        : 'text-slate-800 bg-linear-to-b from-slate-100 via-white to-slate-100'
    ]"
  >
    <CitySelectionModal />
    <Navbar />
    <main class="pt-3 sm:pt-4">
      <router-view />
    </main>
  </div>
</template>