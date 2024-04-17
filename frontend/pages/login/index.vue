<template>
    <VContainer fluid class="fill-height">
      <VRow no-gutters align="center" justify="center" class="fill-height">
        <VCol cols="12" md="6" lg="5" sm="6">
          <VRow no-gutters align="center" justify="center">
            <VCol cols="12" md="6">
              <h1>Sign In</h1>
              <p class="text-medium-emphasis">Enter your details to get started</p>
  
              <VForm @submit.prevent="submit" class="mt-7">
                <div class="mt-1">
                  <label class="label text-grey-darken-2" for="username">Username</label>
                  <VTextField
                    :rules="[ruleRequired, ruleUsername]"
                    v-model="username"
                    prepend-inner-icon="fluent:mail-24-regular"
                    id="username"
                    name="username"
                    type="username"
                  />
                </div>
                <div class="mt-1">
                  <label class="label text-grey-darken-2" for="password">Password</label>
                  <VTextField
                    :rules="[ruleRequired, rulePassword]"
                    v-model="password"
                    prepend-inner-icon="fluent:password-20-regular"
                    id="password"
                    name="password"
                    type="password"
                  />
                </div>
                <div class="mt-5">
                  <VBtn type="submit" block min-height="44" class="gradient primary">Sign In</VBtn>
                </div>
              </VForm>
              <p class="text-body-2 mt-4">
                <span
                  >Don't have an account?
                  <NuxtLink to="/register" class="font-weight-bold text-primary"
                    >Register</NuxtLink
                  ></span
                >
              </p>
            </VCol>
          </VRow>
        </VCol>
        <VCol class="hidden-md-and-down fill-height" md="6" lg="7">
          <VImg
            src="https://wallpaper.dog/large/5557744.jpg"
            cover
            class="h-100 rounded-xl d-flex align-center justify-center"
          >
            <div class="text-center w-50 text-white mx-auto">
              <h2 class="mb-4">Secure Image Gallery</h2>
              <p>
                Lorem, ipsum dolor sit amet consectetur adipisicing elit. Asperiores, inventore quia.
                Dolorum dolores ad ipsum voluptatum rem, hic placeat, odio, odit numquam quod
                veritatis accusantium assumenda! Sequi, provident in! Iure!
              </p>
            </div>
          </VImg>
        </VCol>
      </VRow>
    </VContainer>
  </template>
  
  <script setup>
  import { useUserStore } from '~~/stores/user';

  const userStore = useUserStore()
  const router = useRouter()

  definePageMeta({
        middleware: 'is-logged-in'
    })

  const username = ref(null);
  const password = ref(null);
  let errors = ref(null)
  
  const { ruleUsername, rulePassword, ruleRequired } = useFormRules();
  
  const submit = async () => {
    errors.value = null
        try {
            await userStore.login(username.value, password.value);
            router.push('/gallery')
        } catch (error) {
            errors.value = error.response.errors
        }
  };
  </script>
  