<template>
    <LoaderComp v-if="isLoading" />
    <router-view v-else />
</template>
<script setup lang="ts">
import './styles/global.scss';
import './styles/variables.scss';
import { ref, onMounted } from 'vue';
import LoaderComp from './components/LoaderComp.vue';
import { useRouter } from 'vue-router';
import { getCookie } from './utils/getCookie';

const isLoading = ref(false);
const router = useRouter();
onMounted(()=>{
    if (getCookie('token')) {
        router.push('/home')
    }
    else{
        router.push('/login')
    }
})
</script>
