<template>
    <v-container class="bg-surface-variant">
        <v-sheet class="ma-2 pa-2">
            Welcome to your Gallery
        </v-sheet>
        <v-sheet class="ma-2 pa-2">
                <v-file-input v-model="upload" accept="image/png, image/jpeg, image/gif"
                                    placeholder="Put Image" prepend-icon="mdi-file"
                                    label="Image File">
                </v-file-input>
                <button
                    class="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-md px-2 py-1 text-black" @click="uploadImage">Upload
                </button>
        </v-sheet>
        <v-row no-gutters>
            <v-col v-for="image in images" :key="image.image_id" cols="12" sm="4">
                <v-sheet class="ma-2 pa-2">
                    {{ image.image_name }}
                </v-sheet>
                <v-sheet class="ma-2 pa-2">
                    {{ image.image_id }}
                </v-sheet>
                <NuxtImg fit="contain" width="300" height="200"
                    v-bind:src="'data:' + image.mime_type + ';base64,' + image.image_data" />
                <button class="bg-gradient-to-r from-cyan-500 to-blue-500 rounded-md px-2 py-1 text-white"
                    @click="deleteImage(image.image_id)">Delete</button>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { useUserStore } from '~~/stores/user';

const userStore = useUserStore()
let images = ref("Empty")
let upload = ref()

definePageMeta({
    middleware: 'is-logged-in'
})

onMounted(async () => {
    try {
        await $fetch(
            '/api/v1/image', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userStore.$state.token
            }
        }
        ).then((result) => {
            console.log(result)
            images.value = result.data
        })
    } catch (error) {
        console.log(error)
    }
})

const deleteImage = async (image_id) => {
    try {
        await $fetch(
            '/api/v1/image/' + image_id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + userStore.$state.token
            }
        }
        )
        try {
            await $fetch(
                '/api/v1/image', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + userStore.$state.token
                }
            }
            ).then((result) => {
                console.log(result)
                images.value = result.data
            })
        } catch (error) {
            console.log(error)
        }
    } catch (error) {
        console.log(error)
    }
}

const uploadImage = async () => {
    try {
        const formData = new FormData();
        console.log(upload.value[0])
        formData.append('file', upload.value[0]);
        await $fetch(
            '/api/v1/image', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer ' + userStore.$state.token
            }
        }
        )
        try {
            await $fetch(
                '/api/v1/image', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + userStore.$state.token
                }
            }
            ).then((result) => {
                console.log(result)
                images.value = result.data
            })
        } catch (error) {
            console.log(error)
        }
    } catch (error) {
        console.log(error)
    }
}

</script>