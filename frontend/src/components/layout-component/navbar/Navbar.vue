<script setup>
import { computed, ref, onMounted, onUnmounted, inject } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import logoUrl from '../../../assets/images/bookmyfilm.png'

const route = useRoute()
const router = useRouter()

const theme = inject('theme')
const isDarkMode = computed(() => theme?.isDarkMode?.value ?? false)
const toggleTheme = () => theme?.toggleTheme?.()

const query = computed({
  get: () => (route.query.q ?? '') || '',
  set: (v) => {
    const next = { ...route.query }
    if (v) next.q = v
    else delete next.q
    router.replace({ query: next })
  },
})

const mainCities = [
  'München',
  'Frankfurt',
  'Hamburg',
  'Berlin',
  'Düsseldorf',
]

const otherCities = [
  'Augsburg',
  'Bielefeld',
  'Bonn',
  'Bremen',
  'Dortmund',
  'Dresden',
  'Essen',
  'Freiburg',
  'Göttingen',
  'Halle',
  'Hannover',
  'Heilbronn',
  'Kiel',
  'Köln',
  'Krefeld',
  'Magdeburg',
  'Mülheim',
  'Nuremberg',
  'Offenbach',
  'Oldenburg',
  'Regensburg',
  'Sindelfingen',
  'Stuttgart',
  'Trier',
  'Wolfsburg',
  'Wuppertal',
  'Würzburg',
  'Leipzig',
]

const showDropdown = ref(false)

const getCity = () => localStorage.getItem('selectedCity')

const activeCity = computed(() => (route.query.city ?? '').toString())

function pickLocation(loc) {
  router.replace({ query: { ...route.query, city: loc } })
}

function handleClickOutside(event) {
  if (!event.target.closest('.relative')) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const sunIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>`

const moonIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`
</script>

<template>
  <header
    :class="[
      'sticky top-0 z-50 border-b backdrop-blur-xl transition-all duration-300',
      isDarkMode
        ? 'border-slate-700/40 bg-slate-900/95 shadow-lg shadow-black/20'
        : 'border-slate-200 bg-white/95 shadow-sm'
    ]"
  >
    <div
      class="w-full max-w-7xl mx-auto px-3 sm:px-4 py-3 flex flex-col sm:flex-row sm:items-start gap-3 sm:gap-5"
    >
      <!-- Logo: top-left, large, links home -->
      <RouterLink
        :to="{
          path: '/',
          query: {  
            city: getCity() || "München"
          }
        }"
        :class="[
          'group shrink-0 self-start rounded-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/90 focus-visible:ring-offset-2',
          isDarkMode ? 'focus-visible:ring-offset-slate-900' : 'focus-visible:ring-offset-white'
        ]"
        title="BookMyFilm — Startseite"
      >
      <img
        :src="logoUrl"
        alt="BookMyFilm"
        class="h-16 sm:h-20 md:h-24 w-auto object-contain drop-shadow-[0_2px_6px_rgba(0,0,0,0.4)]"
      />
      </RouterLink>

      <div class="flex-1 min-w-0 w-full flex flex-col gap-2.5">
        <div class="flex items-center gap-2">
          <input
            v-model="query"
            type="text"
            placeholder="Filme oder Kinos suchen…"
            :class="[
              'w-full rounded-full border px-4 py-2.5 text-sm outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/40 transition-colors',
              isDarkMode
                ? 'border-slate-700 bg-slate-800 text-slate-100 placeholder:text-slate-500'
                : 'border-slate-200 bg-slate-50 text-slate-900 placeholder:text-slate-400'
            ]"
          />

          <button
            type="button"
            :class="[
              'shrink-0 rounded-full px-4 py-2.5 text-sm font-semibold transition-colors',
              isDarkMode
                ? 'border-slate-600 text-slate-300 hover:border-slate-500 hover:bg-slate-800'
                : 'border-slate-400 text-slate-700 hover:border-slate-500 hover:bg-slate-100'
            ]"
          >
            Suchen
          </button>

          <!-- Theme Toggle Button -->
          <button
            type="button"
            @click="toggleTheme"
            :class="[
              'shrink-0 rounded-full p-2.5 transition-colors',
              isDarkMode
                ? 'text-yellow-400 hover:bg-slate-800'
                : 'text-slate-600 hover:bg-slate-100'
            ]"
            :title="isDarkMode ? 'Light Mode' : 'Dark Mode'"
          >
            <span v-if="isDarkMode" v-html="sunIcon"></span>
            <span v-else v-html="moonIcon"></span>
          </button>
        </div>

        <div class="flex flex-wrap gap-2">
          <button
            v-for="loc in mainCities"
            :key="loc"
            type="button"
            @click="pickLocation(loc)"
            class="rounded-full border px-3 py-1.5 text-xs font-medium transition"
            :class="[
              activeCity === loc
                ? 'border-blue-600 bg-blue-600 text-white shadow-md'
                : isDarkMode
                  ? 'border-slate-600 bg-slate-700/60 text-slate-200 hover:bg-slate-700'
                  : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-white hover:shadow-sm hover:border-slate-300'
            ]"
          >
            {{ loc }}
          </button>
          
          <!-- Dropdown for other cities -->
          <div class="relative">
            <button
              type="button"
              @click="showDropdown = !showDropdown"
              :class="[
                'rounded-full border px-3 py-1.5 text-xs font-medium transition',
                isDarkMode
                  ? 'border-slate-600 bg-slate-700/60 text-slate-200 hover:bg-slate-600 hover:border-slate-500'
                  : 'border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200 hover:border-slate-400'
              ]"
            >
              Weitere Städte ▼
            </button>
            
            <div
              v-if="showDropdown"
              :class="[
                'absolute top-full mt-1 left-0 border rounded-lg shadow-lg z-50 min-w-36',
                isDarkMode
                  ? 'bg-slate-800 border-slate-600'
                  : 'bg-white border-slate-300'
              ]"
            >
              <button
                v-for="city in otherCities"
                :key="city"
                type="button"
                @click="pickLocation(city); showDropdown = false"
                :class="[
                  'block w-full text-left px-3 py-2 text-xs transition first:rounded-t-lg last:rounded-b-lg',
                  isDarkMode
                    ? 'text-slate-200 hover:bg-slate-700'
                    : 'text-slate-700 hover:bg-slate-50',
                  activeCity === city ? 'bg-blue-500 text-white' : ''
                ]"
              >
                {{ city }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
