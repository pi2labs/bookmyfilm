import { createRouter, createWebHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import MovieDetail from '../pages/MovieDetail.vue'

const routes = [{
        path: '/',
        component: Home
    },
    {
        path: '/movie/:title',
        component: MovieDetail
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router