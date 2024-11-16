<template>
    <div class="sprintComponent">
        <div class="name">
            <div class="circle" :style="{ backgroundColor: generateBrightPastelColor() }"></div>
            <h2>{{ name }}</h2>
        </div>
        <div class="sprintInfo">
            <div class="infoItem">
                <p>Проект</p>
                <h4>{{ project }}</h4>
            </div>
            <div class="infoItem">
                <p>Здоровье</p>
                <div class="health" :style="{ backgroundColor: selectHealthColor(health) }">
                    <CustomIcon id="health" :width="14" :height="14" />
                    {{ health }}
                </div>
            </div>
            <div class="infoItem">
                <p>Прогресс</p>
                <h4>{{ sprintProgress.progressPercentage }}% ({{ sprintProgress.elapsedHours }}/{{ sprintProgress.totalHours }} ч.)</h4>
            </div>
            <div class="infoItem">
                <p>Статус</p>
                <h4>{{ status }}</h4>
            </div>
        </div>
        <div class="progress">
            <div class="runner">
                <CustomIcon
                    id="runner"
                    :width="24"
                    :height="24"
                    :style="{
                        position: 'absolute',
                        left: `calc(${sprintProgress.progressPercentage}% - 15px)`,
                        top: '-2px',
                    }"
                />
                <div class="progressBar">
                    <div class="progressBarInner" :style="{ width: sprintProgress.progressPercentage + '%' }"></div>
                </div>
                <div class="date">
                    <p>{{ formatDateToRus(startDate) }}</p>
                    <p>{{ formatDateToRus(endDate) }}</p>
                </div>
            </div>
            <MainButton text="Подробнее" type="third" size="l" style="width: 100%" />
        </div>
    </div>
</template>
<script setup lang="ts">
import CustomIcon from '@/ui/CustomIcon.vue';
import MainButton from '@/ui/MainButton.vue';
import { formatDateToRus } from '@/utils/formatDateRus';

defineOptions({
    name: 'SprintComponent',
});
const { name, project, health, startDate, endDate } = defineProps<{
    name: string;
    project: string;
    health: string;
    startDate: string;
    endDate: string;
    status: string;
}>();
const generateBrightPastelColor = (): string => {
    let colors = ['#FF8ACE', '#3DEABC', '#A48AFF'];
    return colors[Math.floor(Math.random() * colors.length)];
};

type SprintProgress = {
    progressPercentage: string;
    elapsedHours: string;
    totalHours: string;
};

function calculateSprintProgress(startDate: string | Date, endDate: string | Date, currentDate: string | Date): SprintProgress {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const current = new Date(currentDate);

    // Validate dates
    if (isNaN(start.getTime()) || isNaN(end.getTime()) || isNaN(current.getTime())) {
        throw new Error('Invalid date format');
    }

    // Calculate total sprint duration in milliseconds
    const totalSprintTime = end.getTime() - start.getTime();

    if (totalSprintTime <= 0) {
        throw new Error('End date must be after start date');
    }

    // Calculate total working days in the sprint
    const totalSprintDays = totalSprintTime / (1000 * 3600 * 24);

    // Calculate total working hours (capped at 8 hours per day)
    const totalHours = totalSprintDays * 8;

    // Calculate elapsed time since the start of the sprint
    const elapsedTime = Math.max(0, current.getTime() - start.getTime());

    // Calculate elapsed working days
    const elapsedDays = Math.min(elapsedTime / (1000 * 3600 * 24), totalSprintDays);

    // Calculate elapsed working hours (capped at 8 hours per day)
    const elapsedHours = elapsedDays * 8;

    // Calculate progress percentage
    const progressPercentage = Math.min(100, (elapsedTime / totalSprintTime) * 100);

    return {
        progressPercentage: progressPercentage.toFixed(0), // Rounded to two decimal places
        elapsedHours: elapsedHours.toFixed(0), // Rounded to two decimal places
        totalHours: totalHours.toFixed(0), // Rounded to two decimal places
    };
}
const sprintProgress = calculateSprintProgress(startDate, endDate, new Date());
const selectHealthColor = (health: string): string => {
    switch (health) {
        case 'Высокое':
            return '#97E78A';
        case 'Среднее':
            return '#F2CB8B';
        case 'Низкое':
            return '#F2958B';
        default:
            return '#FF8ACE';
    }
};
</script>
<style lang="scss" scoped>
.sprintComponent {
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
            align-items: flex-start;
            gap: 32px;
            width: 100%;
            align-items: center;
            p {
                width: 100px;
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
            .health {
                display: flex;
                padding: 3px 8px 4px 8px;
                justify-content: center;
                align-items: center;
                gap: 4px;
                border-radius: 8px;

                color: var(--color-base-0, #fff);
                text-align: center;
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 500;
                line-height: 18px; /* 128.571% */
            }
        }
    }
    .progress {
        width: 100%;
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 20px;
        .runner {
            height: 58.634px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            align-self: stretch;
            gap: 12px;
            .progressBar {
                height: 4px;
                width: 100%;
                border-radius: 4px;
                background-color: #e0e2e0;
                justify-content: start;
                .progressBarInner {
                    background-color: #45a3fa;
                    height: 100%;
                }
            }
            .date {
                width: 100%;
                display: flex;
                flex-direction: row;
                justify-content: space-between;
            }
        }
    }
}
</style>
