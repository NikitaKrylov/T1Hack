<template>
    <div class="load" v-if="isLoading">
        <CustomIcon id="logo" :width="400" :height="128" className="logo" />
        <div v-if="isLoading" class="loader">
            <div class="spinner"></div>
        </div>
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
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import MenuComp from '@/components/MenuComp.vue';
import { useScansStore } from '@/store/useScansStore';
const route = useRoute();
const isAiChat = computed(() => route.path.includes('ai_chat'));

const isLoading = ref(true);

const errorTxt = ref<string | null>(null);
const scansStore = useScansStore();

watch(
    () => scansStore.folders,
    (newFolders) => {
        console.log('folders updated:', newFolders);
    },
    { immediate: true },
);

onMounted(async () => {});

const goBack = () => {
    window.history.back();
};
onMounted(() => {
    setTimeout(() => {
        isLoading.value = false;
    }, 2000);
});
</script>

<style lang="scss" scoped>
.mainLayout {
    padding: 0;
    width: 100%;
    height: 100dvh;
    display: flex;
    flex-direction: row;
    gap: 20px;
    align-items: center;

    padding: 40px;
    background-color: #f0f2f0;
}
.load {
    display: flex;
    flex-direction: column;
    gap:30px;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100dvh;
    .loader {
        height: 200px;
        width: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000; /* Поверх всего */
        .spinner {
            width: 100px;
            height: 100px;
            border: 10px solid transparent;
            border-top: 10px solid #45a3fa; /* Цвет загрузчика */
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
    }
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
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
