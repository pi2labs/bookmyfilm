<script setup>
import { ref, onMounted, inject, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showModal = ref(false)

const theme = inject('theme')
const isDarkMode = computed(() => theme?.isDarkMode?.value ?? false)

const mainCities = [
  { key: 'munich', name: 'München', aliases: ['Munich', 'München', 'Muenchen'] },
  { key: 'hamburg', name: 'Hamburg', aliases: ['Hamburg', 'Hamburg-Dammtor', 'Hamburg-Harburg', 'Hamburg-Wandsbek', 'HOLI Hamburg'] },
  { key: 'frankfurt', name: 'Frankfurt', aliases: ['Frankfurt', 'Frankfurt am Main'] },
  { key: 'berlin', name: 'Berlin', aliases: ['Berlin', 'berlin'] },
  { key: 'dusseldorf', name: 'Düsseldorf', aliases: ['Düsseldorf', 'Duesseldorf', 'Dusseldorf'] },
]

const otherCities = [
  { key: 'augsburg', name: 'Augsburg', aliases: ['Augsburg', 'ausgburg'] },
  { key: 'bielefeld', name: 'Bielefeld', aliases: ['Bielefeld', 'bielefeld'] },
  { key: 'bremen', name: 'Bremen', aliases: ['Bremen', 'bremen'] },
  { key: 'dresden', name: 'Dresden', aliases: ['Dresden', 'dresden'] },
  { key: 'essen', name: 'Essen', aliases: ['Essen', 'essen'] },
  { key: 'freiburg', name: 'Freiburg', aliases: ['Freiburg', 'freiburg'] },
  { key: 'goettingen', name: 'Göttingen', aliases: ['Göttingen', 'goettingen'] },
  { key: 'halle', name: 'Halle', aliases: ['Halle', 'halle'] },

  { key: 'stuttgart', name: 'Stuttgart', aliases: ['Stuttgart', 'stuttgart'] },
  { key: 'bonn', name: 'Bonn', aliases: ['Bonn', 'bonn'] },
  { key: 'cologne', name: 'Cologne', aliases: ['Köln', 'Cologne', 'Koeln', 'köln', 'koeln'] },
  { key: 'leipzig', name: 'Leipzig', aliases: ['Leipzig', 'leipzig'] },

  { key: 'hannover', name: 'Hannover', aliases: ['Hannover', 'hannover'] },
  { key: 'nuremberg', name: 'Nuremberg', aliases: ['Nürnberg', 'Nuremberg', 'Nuernberg', 'nürnberg', 'nuernberg'] },
  { key: 'dortmund', name: 'Dortmund', aliases: ['Dortmund', 'dortmund'] },
  
]

function selectCity(cityName) {
  localStorage.setItem('selectedCity', cityName)
  showModal.value = false
  router.push({ path: '/', query: { city: cityName } })
}

onMounted(() => {
  const hasSelectedCity = localStorage.getItem('selectedCity')
  const currentCity = router.currentRoute.value.query.city
  
  if (!hasSelectedCity && !currentCity) {
    showModal.value = true
  }
})
</script>

<template>
  <div
    v-if="showModal"
    class="fixed inset-0 z-100 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
  >
    <div 
      :class="[
        'w-full max-w-2xl rounded-2xl border shadow-2xl overflow-hidden',
        isDarkMode
          ? 'bg-linear-to-b from-slate-800 to-slate-900 border-slate-600'
          : 'bg-linear-to-b from-slate-100 to-white border-slate-300'
      ]"
    >
      <!-- Header -->
      <div 
        :class="[
          'p-6 text-center border-b',
          isDarkMode ? 'border-slate-700' : 'border-slate-200'
        ]"
      >
        <h2 :class="[
          'text-2xl font-bold mb-2',
          isDarkMode ? 'text-white' : 'text-slate-800'
        ]">
          Wähle deine Stadt
        </h2>
        <p :class="[
          'text-sm',
          isDarkMode ? 'text-slate-400' : 'text-slate-600'
        ]">
          Wähle eine Stadt, um Filme und Kinos in deiner Nähe zu entdecken
        </p>
      </div>

      <!-- Main Cities -->
      <div class="p-6">
        <h3 :class="[
          'text-xs font-semibold uppercase tracking-wider mb-4',
          isDarkMode ? 'text-slate-500' : 'text-slate-600'
        ]">
          Hauptstädte
        </h3>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          <button
            v-for="city in mainCities"
            :key="city.key"
            @click="selectCity(city.name)"
            :class="[
              'group relative p-4 rounded-xl border-2 transition-all duration-200',
              isDarkMode
                ? 'border-slate-600 bg-slate-800/50 hover:border-amber-500 hover:bg-slate-700/50'
                : 'border-slate-300 bg-slate-100/50 hover:border-amber-500 hover:bg-slate-200/50'
            ]"
          >
            <span :class="[
              'block text-lg font-semibold transition-colors',
              isDarkMode ? 'text-white group-hover:text-amber-400' : 'text-slate-800 group-hover:text-amber-600'
            ]">
              {{ city.name }}
            </span>
            <span :class="[
              'block text-xs mt-1',
              isDarkMode ? 'text-slate-400' : 'text-slate-500'
            ]">
              {{ city.aliases[0] }}
            </span>
          </button>
        </div>
      </div>

      <!-- Other Cities -->
      <div class="px-6 pb-6">
        <h3 :class="[
          'text-xs font-semibold uppercase tracking-wider mb-4',
          isDarkMode ? 'text-slate-500' : 'text-slate-600'
        ]">
          Weitere Städte
        </h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="city in otherCities"
            :key="city.key"
            @click="selectCity(city.name)"
            :class="[
              'px-4 py-2 rounded-full border text-sm transition-all duration-200',
              isDarkMode
                ? 'border-slate-600 bg-slate-800/50 text-slate-300 hover:border-amber-500 hover:text-amber-400 hover:bg-slate-700/50'
                : 'border-slate-300 bg-slate-100/50 text-slate-700 hover:border-amber-500 hover:text-amber-600 hover:bg-slate-200/50'
            ]"
          >
            {{ city.name }}
          </button>
        </div>
      </div>

      <!-- Footer -->
      <div 
        :class="[
          'p-4 border-t text-center',
          isDarkMode
            ? 'bg-slate-900/50 border-slate-700'
            : 'bg-slate-50/50 border-slate-200'
        ]"
      >
        <p :class="[
          'text-xs',
          isDarkMode ? 'text-slate-500' : 'text-slate-600'
        ]">
          Du kannst die Stadt später oben in der Leiste ändern
        </p>
      </div>
    </div>
  </div>
</template>
