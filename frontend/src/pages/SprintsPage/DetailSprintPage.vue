<template>
    <main class="detailPage">
        <DateRangeSlider />
    </main>
</template>
<script setup lang="ts">
import { Sprint } from '@/api/sprintsApi';
import DateRangeSlider from '@/ui/DateRangeSlider.vue';
import MainButton from '@/ui/MainButton.vue';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'DetailSprintPage',
});

const router = useRouter();
const fetchError = ref('');
const sprint = ref<Sprint>();
const goToSprints = () => {
    router.push('/sprints');
};

onMounted(() => {
   
});
</script>
<style lang="scss" scoped>
.detailPage {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 40px;
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    border-radius: 16px;
    background: var(--White-100, #fff);

    

}
</style>
