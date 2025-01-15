<template>
    <main class="px-8 py-6 bg-gray-100">
            <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
                <div class="main-left col-span-2">
                    <div class="p-12 bg-white border border-gray-200 rounded-lg">
                        <h1 class="mb-6 text-2xl">Log in</h1>

                        <p class="mb-6 text-gray-500">
                            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                            Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                        </p>

                        <p class="font-bold">
                            Don't have an account? <RouterLink to="signup" class="underline">Click here</RouterLink> to sign up!
                        </p>
                    </div>
                </div>

                <div class="main-center col-span-2 space-y-4">
                    <div class="p-12 bg-white border border-gray-200 rounded-lg">
                        <form class="space-y-6" v-on:submit.prevent="submitForm()">
                            <div>
                                <label>E-mail</label><br>
                                <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                            </div>

                            <div>
                                <label>Password</label><br>
                                <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                            </div>

                            <template v-if="errors.length > 0">
                                <div class="bg-red-300 text-white rounded-lg p-6">
                                    <p v-for="error in errors" v-bind:key="error">
                                        {{ error }}
                                    </p>
                                </div>
                            </template>

                            <div>
                                <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </main>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: { //data entered by the user. Bound to data on form because of v-model.
                email: '',
                password: '',
            },
            
            errors: [],
        }
    },

    methods: {
        async submitForm() { //called when form is submitted because of v-on:submit
            this.errors = []

            //frondend (client-side) validation
            if (this.form.email === ''){
                this.errors.push('your email is missing')
            }

            if (this.form.password === ''){
                this.errors.push('your password is missing')
            }

            if (this.errors.length ===0) {
                await axios
                    .post ('/api/login/', this.form) //form data is sent to server
                    .then(response => { //server response. Login url returns a token
                        this.userStore.setToken(response.data) //saves token in the store
                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                    })
                    .catch(error => { //stops async function execution if error is caught
                        console.log('error', error)
                    })

                await axios
                    .get('/api/me/')    
                    .then(response => {
                        this.userStore.setUserInfo(response.data) //update user info in the store
                        this.$router.push('/feed') //redirect user to feed page
                    })  
                    .catch(error => {
                        console.log('error', error)
                    })  
            }
        }
    }
}
</script>