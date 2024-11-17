<template>
    <div class="teamComponent">
        <div class="name">
            <div class="circle" :style="{ backgroundColor: generateBrightPastelColor() }"></div>
            <h2>{{ name }}</h2>
        </div>
        <div class="sprintInfo">
            <div class="infoItem">
                <p>Количество участников</p>
                <h4>{{ teammates }} чел.</h4>
            </div>
            <div class="infoItem">
                <p>Количество спринтов</p>
                <h4>{{ sprintsCount }} шт.</h4>
            </div>
        </div>
        <MainButton text="Подробнее" type="third" size="l" style="width: 100%" />
    </div>
</template>
<script setup lang="ts">
import MainButton from '@/ui/MainButton.vue';

defineOptions({
    name: 'TeamComponent',
});
const { name, teammates, sprintsCount } = defineProps<{
    name: string;
    teammates: string;
    sprintsCount: string;
}>();
const generateBrightPastelColor = (): string => {
    let colors = ['#FF8ACE', '#3DEABC', '#A48AFF'];
    return colors[Math.floor(Math.random() * colors.length)];
};
</script>
<style lang="scss" scoped>
.teamComponent {
    display: flex;
    width: 328px;
    padding: 24px;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 24px;
    border-radius: 12px;
    background: #fafafa;
    .name {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
        .circle {
            height: 16px;
            width: 16px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        h2 {
            color: var(--color-base-875, #202220);
            font-family: Inter;
            font-size: 18px;
            font-style: normal;
            font-weight: 500;
            line-height: 24px; /* 133.333% */
            width: fit-content;
            text-wrap: wrap;
        }
    }
    .sprintInfo {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
        width: 100%;
        .infoItem {
            display: flex;
            justify-content: space-between;
            width: 100%;
            align-items: center;
            p {
                width: fit-content;
                color: var(--Base-625, #606260);
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 400;
                line-height: 18px; /* 128.571% */
            }
            h4 {
                color: var(--Base-875, #202220);
                text-align: center;
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 500;
                line-height: 18px; /* 128.571% */
            }
        }
    }
    
}
</style>
