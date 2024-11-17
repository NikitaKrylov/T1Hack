<template>
    <main class="sprintsPage">
        <div class="actualSprints">
            <div class="sectionHeader">
                <h3>Все спринты</h3>
                <div class="btnsGrp">
                    <MainButton text="Загрузить спринт" type="primary" icon="plus" style="width: 217px" size="l" @click="goToAddSprint" />
                </div>
            </div>
            <div class="sprints">
                <SprintComponent
                    v-for="sprint in sprints"
                    :key="sprint.id"
                    :name="sprint.name"
                    project="Хакатон Т1"
                    :start-date="sprint.started_at"
                    :end-date="sprint.finished_at"
                    health="Высокое"
                    :status="sprint.sprint_status"
                    @click="router.push(`/sprints/${sprint.id}`)"
                />
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
import { Sprint, useGetSprints } from '@/api/sprintsApi';
import SprintComponent from '@/components/SprintComponent.vue';
import MainButton from '@/ui/MainButton.vue';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'SprintsPage',
});

const { mutateAsync: getSprints } = useGetSprints();
const router = useRouter();
const fetchError = ref('');
const sprints = ref<Sprint[]>([]);
const goToAddSprint = () => {
    router.push('/sprints/add');
};
const getAllSprints = async () => {
    try {
        const response = await getSprints();
        if (response) {
            sprints.value = response;
            console.log(sprints.value);
        }
    } catch (error: any) {
        fetchError.value = error?.response?.data?.detail || 'Произошла ошибка при входе';
    }
};
onMounted(() => {
    getAllSprints();
});
</script>
<style lang="scss" scoped>
.sprintsPage {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 40px;
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    border-radius: 16px;
    background: var(--White-100, #fff);

    .actualSprints {
        display: flex;
        flex-direction: column;
        gap: 32px;
        width: 100%;
        overflow: hidden;
        .sectionHeader {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: flex-end;
            width: 100%;
            h3 {
                color: var(--color-base-875, #202220);
                font-family: Inter;
                font-size: 24px;
                font-style: normal;
                font-weight: 600;
                line-height: normal;
                width: fit-content;
            }
            .btnsGrp {
                display: flex;
                flex-direction: row;
                gap: 8px;
            }
        }
        .sprints {
            display: flex;
            align-items: flex-start;
            align-content: flex-start;
            gap: 20px;
            flex-wrap: wrap;
            overflow: auto;
        }
        .sprints::-webkit-scrollbar {
            background-color: transparent;
            color: #45a3fa;
            width: 4px;
        }
        .sprints::-webkit-scrollbar-thumb {
            background-color: #45a3fa;
            width: 2px;
            color: black;
        }
    }
}
</style>
