<template>
    <main class="px-8 py-6 bg-gray-100">
            <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
                <div class="main-left col-span-2">
                    <div class="p-12 bg-white border border-gray-200 rounded-lg">
                        <h1 class="mb-6 text-2xl">Edit Profile</h1>

                        <p class="mb-6 text-gray-500">
                            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                        </p>
                    </div>
                </div>

                <div class="main-center col-span-2 space-y-4">
                    <div class="p-12 bg-white border border-gray-200 rounded-lg">
                        <form class="space-y-6" v-on:submit.prevent="submitForm()">
                            <div>
                                <label>Name</label><br>
                                <input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                            </div>

                            <div>
                                <label>E-mail</label><br>
                                <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                            </div>

                            <template v-if="errors.length > 0">
                                <div class="bg-red-300 text-white rounded-lg p-6">
                                    <p v-for="error in errors" v-bind:key="error">
                                        {{ error }}
                                    </p>
                                </div>
                            </template>

                            <div>
                                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Changes</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </main>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: { //data entered by the user. Bound to data on form because of v-model.
                email: this.userStore.user.email,
                name: this.userStore.user.name,
            },

            errors: [],
        }
    },

    methods: {
        submitForm(){ //called when form is submitted because of v-on:submit
            this.errors = [] 
            
            //frondend (client-side) validation
            if (this.form.email === ''){
                this.errors.push('your email is missing')
            }

            if (this.form.name === ''){
                this.errors.push('your name is missing')
            }

            if (this.errors.length ===0) {
                axios
                    .post ('/api/signup/', this.form) //form data is sent to server
                    .then(response => { //server response
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The information was saved', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                        } 
                        else {
                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        } 
    }           
}
</script>