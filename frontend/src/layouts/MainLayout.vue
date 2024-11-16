<template>
    <div class="load" v-if="isLoading">
        <CustomIcon id="logo" :width="207" :height="33" className="logo" />
        <h1 v-if="isLoading && userStore.user">
            Привет, <span>{{ userStore.user?.first_name }}</span>
        </h1>
    </div>
    <div class="mainLayout" v-else-if="!isLoading">
        <MenuComp v-if="!isAiChat" />
        <router-view />
    </div>
    <div class="error" v-else>
        <h1>{{ errorTxt }}</h1>
        <button @click="goBack">Вернуться назад</button>
    </div>
</template>

<script setup lang="ts">
defineOptions({
    name: 'MainLayout',
});
import CustomIcon from '@/ui/CustomIcon.vue';
import { computed, onMounted, ref, toRaw, watch } from 'vue';
import { Doctor, Folder, Patient, useUserStore } from '@/store/useUserStore';
import { useRoute, useRouter } from 'vue-router';
import MenuComp from '@/components/MenuComp.vue';
import { useRoleStore } from '@/store/useRoleStore';
import { useScansStore } from '@/store/useScansStore';
const route = useRoute();
const isChats = computed(() => route.path.includes('chats'));
const isAiChat = computed(() => route.path.includes('ai_chat'));
const applyStyle = computed(() => !route.path.includes('chats') && !route.path.includes('ai_chat'));

const userStore = useUserStore();
const isLoading = ref(true);
const router = useRouter();
const roleStore = useRoleStore();
const errorTxt = ref<string | null>(null);
const scansStore = useScansStore();

watch(
    () => scansStore.folders,
    (newFolders) => {
        console.log('folders updated:', newFolders);
    },
    { immediate: true },
);

onMounted(async () => {
});

const goBack = () => {
    window.history.back();
};
onMounted(() => {
    setTimeout(() => {
        isLoading.value = false;
    }, 3000);
});
</script>

<style lang="scss" scoped>
.mainLayout {
    padding: 0; 
    width: 100%;
    height: 100dvh;
    display: flex;
    flex-direction: row;
    gap:20px;
    align-items: center;
    
    padding: 40px;
    background-color: #F0F2F0;
}
.load {
    width: 100%;
    padding-top: 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    .logo {
        position: relative;
        width: 207px;
        height: 33px;
        z-index: 6;
    }

    h1 {
        margin-top: 209px;
        color: var(--Text, #1d1d1d);
        font-family: var(--font-main);
        font-size: 36px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;

        // Анимация всплытия
        opacity: 0;
        transform: translateY(20px);
        animation: fadeUp 0.8s ease-out forwards;

        span {
            display: inline-block;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeUp 0.8s ease-out forwards;
            animation-delay: 0.4s; // Задержка для анимации span
        }
    }
}
.error {
    width: 100%;
    padding-top: 36px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100dvh;
    gap: 20px;
    font-family: var(--font-main);
    button {
        padding: 10px 20px;
        font-size: 1rem;
        cursor: pointer;
        background-color: #1c274c;
        color: white;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;

        &:hover {
            background-color: #16203c; /* Темнее при наведении */
        }
    }
    h1 {
        margin-top: 209px;
        color: var(--color-main);
        font-family: var(--font-main);
        font-size: 36px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        text-align: center;
        // Анимация всплытия
        opacity: 0;
        transform: translateY(20px);
        animation: fadeUp 0.8s ease-out forwards;
    }
}

// Определение анимации
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
