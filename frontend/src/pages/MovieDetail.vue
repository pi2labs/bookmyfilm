<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const movie = ref(null)
/** null = show all dates in range */
const selectedDate = ref(null)

function localDateISO(d) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

const dateChips = computed(() => {
  if (!movie.value) return []

  const today = new Date()
  const todayBase = new Date(today.getFullYear(), today.getMonth(), today.getDate())

  const release = movie.value.release_date
    ? new Date(movie.value.release_date)
    : null

  const releaseBase = release
    ? new Date(release.getFullYear(), release.getMonth(), release.getDate())
    : null

  // 🔥 KEY LOGIC
  const base =
    releaseBase && releaseBase > todayBase
      ? releaseBase
      : todayBase

  return Array.from({ length: 5 }, (_, i) => {
    const d = new Date(base)
    d.setDate(base.getDate() + i)

    const iso = localDateISO(d)

    let label

    if (base.getTime() === todayBase.getTime()) {
      // normal behavior
      if (i === 0) label = 'Heute'
      else if (i === 1) label = 'Morgen'
      else {
        label = d.toLocaleDateString('de-DE', {
          weekday: 'short',
          day: 'numeric',
          month: 'short',
        })
      }
    } else {
      // 🔥 FUTURE RELEASE → no Heute/Morgen
      label = d.toLocaleDateString('de-DE', {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
      })
    }

    return { iso, label }
  })
})

async function loadMovie() {
  const params = {}
  if (route.query.city) params.city = route.query.city
  const res = await api.get(`/movies/${route.params.title}`, { params })
  movie.value = res.data
}

watch(
  () => [route.params.title, route.query.city],
  () => {
    loadMovie()
  },
  { immediate: true }
)

watch(
  () => dateChips.value,
  (chips) => {
    if (chips.length && !selectedDate.value) {
      selectedDate.value = chips[0].iso
    }
  },
  { immediate: true }
)

const filteredByDate = computed(() => {
  if (!movie.value?.showtimes_by_date) return []
  const rows = movie.value.showtimes_by_date
  if (!selectedDate.value) return rows
  return rows.filter((r) => r.date === selectedDate.value)
})

function headingForDate(dateStr) {
  const c = dateChips.value.find((x) => x.iso === dateStr)
  if (c) return c.label
  const d = new Date(`${dateStr}T12:00:00`)
  return d.toLocaleDateString('de-DE', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  })
}
</script>

<template>
  <div v-if="movie" class="p-6 max-w-6xl mx-auto">

    <div class="flex gap-6 mb-8">
      <img
        :src="movie.poster_url"
        width="120"
        height="100"
        class="w-[120px] h-[100px] object-cover rounded-lg shadow-lg shadow-black/40 ring-1 ring-slate-700 shrink-0"
      />

      <div>
        <h1 class="text-3xl font-bold text-slate-50">{{ movie.title }}</h1>
        <p v-if="movie.release_date" class="text-blue-400 text-sm mb-2">
          Ab {{ new Date(movie.release_date).toLocaleDateString('de-DE') }}
        </p>
        <p class="text-slate-400 mt-2">{{ movie.duration }} • {{ movie.genres }}</p>

        <a
          v-if="movie.trailer_url"
          :href="movie.trailer_url"
          target="_blank"
          class="text-amber-400 hover:text-amber-300 mt-3 inline-block"
        >
          ▶ Trailer
        </a>
      </div>
    </div>

    <h2 class="text-lg font-semibold text-slate-100 mb-2">
      Vorstellungen
    </h2>

    <div class="flex flex-wrap gap-2 mb-6">
      <button
        type="button"
        class="rounded-full border px-3 py-1.5 text-sm font-medium transition"
        :class="
          selectedDate === null
            ? 'border-blue-500 bg-blue-500 text-white shadow-sm'
            : 'border-slate-500 bg-slate-700/60 text-slate-200 hover:bg-slate-700 hover:border-slate-400'
        "
        @click="selectedDate = null"
      >
        Alle Tage
      </button>
      <button
        v-for="chip in dateChips"
        :key="chip.iso"
        type="button"
        class="rounded-full border px-3 py-1.5 text-sm font-medium transition"
        :class="
          selectedDate === chip.iso
            ? 'border-blue-500 bg-blue-500 text-white shadow-sm'
            : 'border-slate-500 bg-slate-700/60 text-slate-200 hover:bg-slate-700 hover:border-slate-400'
        "
        @click="selectedDate = chip.iso"
      >
        {{ chip.label }}
      </button>
    </div>

    <div v-if="!filteredByDate.length" class="text-slate-500 py-6">
      Keine Vorstellungen für diese Auswahl.
    </div>

    <div v-for="day in filteredByDate" :key="day.date" class="mb-10">
      <h3 class="text-xl font-semibold mb-4 text-slate-50">
        {{ headingForDate(day.date) }}
        <span class="text-sm font-normal text-slate-500 ml-2">{{ day.date }}</span>
      </h3>

      <div
        v-for="(shows, theater) in day.theaters"
        :key="theater"
        class="mb-6"q
      >
        <h4 class="text-base font-semibold mb-2 text-slate-300">
          {{ theater }}
        </h4>

        <div class="flex flex-wrap gap-3">
          <a
            v-for="show in shows"
            :key="show.start_time + show.screen + show.booking_url"
            :href="show.booking_url"
            target="_blank"
            class="border border-slate-600 bg-slate-800/50 px-3 py-2 rounded-lg hover:border-amber-500/40 hover:bg-slate-800 transition"
          >
            <div class="font-medium text-slate-100">
              {{ show.start_time }}
            </div>
            <div class="text-sm text-slate-400">
              {{ show.screen }} •  ab {{ show.price }}€
            </div>
            <div class="text-xs text-slate-500">
              {{ show.language }}
            </div>
            <div class="text-xs text-slate-500">
              {{ show.formats.join(', ') }}
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
