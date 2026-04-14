<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import logoUrl from '../../../assets/images/bookmyfilm.png'

const route = useRoute()
const router = useRouter()

const query = computed({
  get: () => (route.query.q ?? '') || '',
  set: (v) => {
    const next = { ...route.query }
    if (v) next.q = v
    else delete next.q
    router.replace({ query: next })
  },
})

const locations = [
  'Munich',
  'Hamburg',
  'Frankfurt',
  'Berlin',
  'Stuttgart',
  'Bonn',
  'Düsseldorf',
]

const activeCity = computed(() => (route.query.city ?? '').toString())

function pickLocation(loc) {
  router.replace({ query: { ...route.query, city: loc } })
}

function clearCity() {
  const { city: _c, ...rest } = route.query
  router.replace({ query: rest })
}
</script>

<template>
  <header
    class="sticky top-0 z-50 border-b border-amber-500/20 bg-slate-800/80 backdrop-blur-xl border-b border-slate-600//40 shadow-[0_4px_30px_rgba(0,0,0,0.5)] backdrop-blur-md"
  >
    <div
      class="w-full max-w-7xl mx-auto px-3 sm:px-4 py-3 flex flex-col sm:flex-row sm:items-start gap-3 sm:gap-5"
    >
      <!-- Logo: top-left, large, links home -->
      <RouterLink
        to="/"
        class="group shrink-0 self-start rounded-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400/90 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
        title="BookMyFilm — Startseite"
      >
      <img
        :src="logoUrl"
        alt="BookMyFilm"
        class="h-16 sm:h-20 md:h-24 w-auto object-contain drop-shadow-[0_2px_6px_rgba(0,0,0,0.6)]"
      />
      </RouterLink>

      <div class="flex-1 min-w-0 w-full flex flex-col gap-2.5">
        <div class="flex items-center gap-2">
          <input
            v-model="query"
            type="text"
            placeholder="Filme oder Kinos suchen…"
            class="w-full rounded-full border border-slate-600/80 bg-slate-800/70 px-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/40"
          />

          <button
            type="button"
            class="shrink-0 rounded-full border-slate-500 px-4 py-2.5 text-sm font-semibold text-slate-200 hover:border-slate-400 transition-colors"
          >
            Suchen
          </button>
        </div>

        <div class="flex flex-wrap gap-2">
          <button
            type="button"
            @click="clearCity()"
            class="rounded-full border px-3 py-1.5 text-xs font-medium transition"
            :class="
              !activeCity
                  ? 'border-blue-500 bg-blue-500 text-white shadow-sm'
                  : 'border-slate-500 bg-slate-700/60 text-slate-200 hover:bg-slate-700 hover:border-slate-400'
              "
          >
            Alle Städte
          </button>
          <button
            v-for="loc in locations"
            :key="loc"
            type="button"
            @click="pickLocation(loc)"
            class="rounded-full border px-3 py-1.5 text-xs font-medium transition"
            :class="
              activeCity === loc
                ? 'border-blue-500 bg-blue-500 text-white shadow-sm'
                : 'border-slate-500 bg-slate-700/60 text-slate-200 hover:bg-slate-700 hover:border-slate-400'
            "
          >
            {{ loc }}
          </button>
        </div>
      </div>
    </div>
  </header>
</template>
