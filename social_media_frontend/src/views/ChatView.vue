<template>
    chat
</template>

<script>
import axios from 'axios';

export default {
    name: 'chat',

    mounted(){
        this.GetConversations()
    },

    methods: {
        GetConversations(){
            console.log('GetConversations')
            axios
                .get('/api/chat/')
                .then( response => {
                    console.log(response.data)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>