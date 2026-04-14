<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const movies = ref([])
const route = useRoute()
const router = useRouter()

async function loadMovies() {
  const params = {}
  if (route.query.city) {
    params.city = route.query.city
  }
  const res = await api.get('/movies', { params })
  movies.value = res.data
}

watch(
  () => route.query.city,
  () => {
    loadMovies()
  },
  { immediate: true }
)

function slugForMovie(movie) {
  return movie.slug || slugifyFallback(movie.title)
}

function slugifyFallback(title) {
  return String(title)
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
}

function goToMovie(movie) {
  const q = { ...route.query }
  router.push({
    path: `/movie/${slugForMovie(movie)}`,
    query: q,
  })
}

function genreLabel(genres) {
  if (!genres || !String(genres).trim()) return ''
  return String(genres)
}
</script>

<template>
  <div class="w-full max-w-7xl mx-auto px-2 sm:px-4 py-6">

    <div class="flex flex-col lg:flex-row gap-6">

      <div class="flex-1 min-w-0 w-full">
        <div
          class="flex flex-row flex-nowrap gap-5 sm:gap-4 overflow-x-auto overflow-y-hidden w-full min-w-0 pb-2 scroll-smooth snap-x snap-mandatory [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
          <div
            v-for="movie in movies"
            :key="movie.id"
            class="cursor-pointer group shrink-0 w-[180px] snap-start text-left"
            @click="goToMovie(movie)"
          >
            <div class="relative w-[180px] rounded-lg overflow-hidden shadow-md ring-1 ring-black/10 bg-black">

              <img
                :src="movie.poster_url"
                width="180"
                height="320"
                alt=""
                class="w-[180px] h-[320px] object-cover block group-hover:opacity-95 transition-opacity"
              />

              <div
                v-if="movie.rating != null && movie.rating !== ''"
                class="absolute bottom-0 left-0 right-0 bg-black text-white text-[11px] sm:text-xs flex items-center px-2 py-1.5"
              >
                <span class="flex items-center gap-0.5 min-w-0">
                  <span class="text-red-500 shrink-0" aria-hidden="true">★</span>
                  <span class="font-medium truncate">{{ movie.rating }}/10</span>
                </span>
              </div>
            </div>

            <p class="mt-2 text-sm font-bold text-slate-100 leading-snug line-clamp-2">
              {{ movie.title }}
            </p>
            <p v-if="movie.release_date" class="text-slate-400">
              Ab {{ new Date(movie.release_date).toLocaleDateString('de-DE') }}
            </p>
            <p
              v-if="genreLabel(movie.genres)"
              class="mt-0.5 text-xs text-slate-400 line-clamp-2"
            >
              {{ genreLabel(movie.genres) }}
            </p>
          </div>
        </div>

        <div class="my-10 text-center border border-slate-700/80 bg-slate-900/40 p-6 rounded-xl">
          <p class="text-slate-500">Ad Space</p>
        </div>
      </div>

      <div class="w-full lg:w-64 shrink-0 space-y-6 hidden lg:block">

        <div class="border border-slate-700/80 bg-slate-900/40 p-6 text-center rounded-xl">
          <p class="text-slate-500">Ad Space</p>
        </div>

        <div class="border border-slate-700/80 bg-slate-900/40 p-6 text-center rounded-xl">
          <p class="text-slate-500">Ad Space</p>
        </div>
      </div>

    </div>

  </div>
</template>
