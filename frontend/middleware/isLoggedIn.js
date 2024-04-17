import { useUserStore } from '~~/stores/user'

export default defineNuxtRouteMiddleware((to, from) => {
    const userStore = useUserStore()
    
    if (to.fullPath === '/login' && userStore.$state.isLoggedIn) {
        return navigateTo('/gallery')
    }

    if (to.fullPath === '/register' && userStore.$state.isLoggedIn) {
        return navigateTo('/gallery')
    }

    if (to.fullPath === '/' && userStore.$state.isLoggedIn) {
        return navigateTo('/gallery')
    }

    if (to.fullPath === '/gallery' && userStore.$state.isLoggedIn == false) {
        return navigateTo('/login')
    }
})