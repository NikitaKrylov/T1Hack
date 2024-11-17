<template>
    <router-view />
</template>
<script setup lang="ts">
import './styles/global.scss';
import './styles/variables.scss';
import '@gravity-ui/uikit/styles/fonts.css';
import '@gravity-ui/uikit/styles/styles.css';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getCookie } from './utils/getCookie';

const router = useRouter();
onMounted(()=>{
    if (getCookie('token')) {
        router.push('/sprints')
    }
    else{
        router.push('/login')
    }
})
</script>
