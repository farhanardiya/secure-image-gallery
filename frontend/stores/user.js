import { defineStore } from "pinia";

export const useUserStore = defineStore('user', {
    state: () => ({
        token: '',
        isLoggedIn: false,
    }),
    actions: {
        async login(username, password) {
            await $fetch('/api/v1/login', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
              }).then((result) => {
                console.log(result)
                localStorage.setItem('token',result.data.token)
                this.$state.token = result.data.token
                this.$state.isLoggedIn = true;
            });
        },
        
        async register(username, password) {
            await $fetch('/api/v1/register', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ username, password })
            })
        },
      
        async logout() {
            // await $axios.post('/api/v1/logout')
            this.resetState()
        },

        resetState() {      
            this.$state.token = ''
            this.$state.isLoggedIn = false
        },
    },
    persist: true,
})