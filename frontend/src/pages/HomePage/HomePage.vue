<template>
    <main class="homePage">
        <div class="actualSprints">
            <div class="sectionHeader">
                <h3>Актуальные спринты</h3>
                <MainButton text="Создать спринт" type="secondary" icon="plus" style="width: 182px" size="l" @click="goToAddSprint"/>
            </div>
            <div class="sprints">
                <SprintComponent
                    name="Спринт 2024.3.1.NPP Shared Sprint"
                    project="Хакатон Т1"
                    start-date="2024-11-15"
                    end-date="2024-11-29"
                    health="Высокое"
                    status="Активный"
                />
                <SprintComponent
                    name="Спринт 2024.3.1.NPP Shared Sprint"
                    project="Хакатон Т1"
                    start-date="2024-11-15"
                    end-date="2024-11-29"
                    health="Среднее"
                    status="Активный"
                />
                <SprintComponent
                    name="Спринт 2024.3.1.NPP Shared Sprint"
                    project="Хакатон Т1"
                    start-date="2024-11-15"
                    end-date="2024-11-29"
                    health="Низкое"
                    status="Активный"
                />
                <SprintComponent
                    name="Спринт 2024.3.1.NPP Shared Sprint"
                    project="Хакатон Т1"
                    start-date="2024-11-15"
                    end-date="2024-11-29"
                    health="Высокое"
                    status="Активный"
                />
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
import SprintComponent from '@/components/SprintComponent.vue';
import MainButton from '@/ui/MainButton.vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'HomePage',
});
const router = useRouter();
const goToAddSprint = () => {
    router.push('/sprints/add');
}
</script>
<style lang="scss" scoped>
.homePage {
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
        }
        .sprints {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            row-gap: 20px;
            gap: 10px;
        }
    }
}
</style>
