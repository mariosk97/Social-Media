<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink> <!--name refers to component name in index.js NOT url.py-->
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>
                <div class="mt-6">
                    <button 
                        class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id">
                        Send friendship request
                    </button>

                    <button 
                        class="inline-block mt-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id">
                        Send message
                    </button>

                    <RouterLink 
                        class="inline-block py-4 mr-2 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        to="/profile/edit"
                        v-if="userStore.user.id == user.id">
                        Edit Profile
                    </RouterLink>

                    <button 
                        class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                        @click="logout"
                        v-if="userStore.user.id == user.id">
                        Logout
                    </button>
                </div>
            </div>
        </div>
     
        <div class="main-center col-span-2 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg"
            v-if="userStore.user.id === user.id" 
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" /> 
            </div>
        </div>    

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow/>
            <Trends/>    
        </div>
    </div>    
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import { useUserStore } from '@/stores/user'
import FeedItem from '@/components/FeedItem.vue';
import { useToastStore } from '@/stores/toast'

export default {
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },       

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            posts: [],
            user: {},
            body: '', //connected with v-model to textarea
        }
    },

    mounted() { //Calls the getFeed method after the component is mounted to load the feed
        this.getFeed()
    },

    watch: { 
        '$route.params.id': { //watching the id in the route. Whole page does not reload when switching to different profile.
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        sendDirectMessage() {
            console.log('sendDirectMessage')
            axios   
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    console.log('data', response.data)
                    this.$router.push('/chat')
                })   
                .catch(error => {
                    console.log('error', error)
                })   
        },
        sendFriendshipRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`) //send friend request
                .then(response => {
                    console.log('data', response.data)

                    if (response.data.message == 'request already sent'){
                        this.toastStore.showToast(5000, 'The request has already been sent', 'bg-red-300')
                    }    
                    else{
                        this.toastStore.showToast(5000, 'The request was sent', 'bg-emerald-300')
                    }
                })  
                .catch(error => {
                    console.log('error', error)
                })  
        },
        
        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`) //show users posts
                .then(response => {
                    console.log('data', response.data.posts)
                    this.posts = response.data.posts
                    this.user = response.data.user
                })    
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() { //post on your feed
            console.log('submitform', this.body)
            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)
                    this.posts.unshift(response.data) //adds the post to the top of the list
                    this.body = '' //clear users text box
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log("logout")
            this.userStore.removeToken()
            this.$router.push('/login')
        }
    }
}
</script>