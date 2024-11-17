<template>
    <main class="detailPage" v-if="sprint">
        <div class="detailPageHeader">
            <div class="sprintInfo">
                <button class="back" @click="goToSprints"><CustomIcon id="arrow_back" :width="16" :height="16" /></button>
                <div class="name">
                    <div class="circle" :style="{ backgroundColor: generateBrightPastelColor() }"></div>
                    <h2>{{ sprint?.name }}</h2>
                </div>
            </div>
            <div class="filters">
                <DateRangeSlider
                    :endDateInput="sprint.finished_at"
                    :startDateInput="sprint.started_at"
                    v-model:startDate="startDate"
                    v-model:endDate="endDate"
                />
                <MainButton text="Применить фильтры" type="primary" size="l" style="width: 200px" @click="handleFetchMetrics" />
            </div>
        </div>
        <div class="detailPageBody" v-if="metrix.KPI_total_tasks > 0">
            <div class="healthMetric">
                <img :src="`/img/health-${sprintHealth}.svg`" />
            </div>
            <div class="kpiMetrics">
                <div class="metric">
                    <p>Всего задач на спринте</p>
                    <h5>{{ metrix?.KPI_total_tasks }}</h5>
                </div>
                <div class="metric">
                    <p>Выполнено задач</p>
                    <h5>{{ metrix?.KPI_completed_tasks }}</h5>
                </div>
                <div class="metric">
                    <p>Заблокировано задач в Ч/Д</p>
                    <h5>{{ metrix?.blockedtasksCHD_metric }}</h5>
                </div>
            </div>
            <div class="taskStatus">
                <h3>Состояние задач</h3>
                <Pie :data="pieChartData" :options="pieChartOptions" />
            </div>
            <div class="taskStatusText">
                <div class="textMetric">
                    <p>Cделано</p>
                    <h5>{{ metrix?.sdelano_metric[0] }}</h5>
                    <DonutComp :percentage="metrix?.sdelano_metric[1]" />
                </div>
                <div class="textMetric">
                    <p>Снято</p>
                    <h5>{{ metrix?.snyato_metric[0] }}</h5>
                    <DonutComp :percentage="metrix?.snyato_metric[1]" />
                </div>
                <div class="textMetric">
                    <p>В работе</p>
                    <h5>{{ metrix?.vrabote_metric[0] }}</h5>
                    <DonutComp :percentage="metrix?.vrabote_metric[1]" />
                </div>
                <div class="textMetric">
                    <p>К выполнению</p>
                    <h5>{{ metrix?.kvipolneniyu_metric[0] }}</h5>
                    <DonutComp :percentage="metrix?.kvipolneniyu_metric[1]" />
                </div>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
defineOptions({
    name: 'DetailSprintPage',
});
import { Sprint, useGetMetrics, useGetSprint } from '@/api/sprintsApi';
import api from '@/api/baseApi';
import CustomIcon from '@/ui/CustomIcon.vue';
import DateRangeSlider from '@/ui/DateRangeSlider.vue';
import MainButton from '@/ui/MainButton.vue';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';

import { computed, onMounted, reactive, ref, toRaw, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import DonutComp from '@/components/DonutComp.vue';
const sprintHealth = computed(() => {
    if (metrix.health > 0 && metrix.health < 33) {
        return 'danger';
    }
    else if (metrix.health > 33 && metrix.health < 66) {
        return 'medium';
    }
    else {
        return 'good';
    }
})
ChartJS.register(ArcElement, Tooltip, Legend);
// Тип для метрик
interface Metrics {
    KPI_total_tasks: number;
    KPI_completed_tasks: number;
    blockedtasksCHD_metric: number;
    sdelano_metric: number[];
    vrabote_metric: number[];
    snyato_metric: number[];
    kvipolneniyu_metric: number[];
    [key: string]: any;
}

const router = useRouter();
const route = useRoute();

const sprint = ref<Sprint | null>(null);
const sprintID = ref<number>(0);
const startDate = ref<string>(sprint.value?.started_at || '');
const endDate = ref<string>(sprint.value?.finished_at || '');
const metrix = reactive<Metrics>({
    KPI_total_tasks: 0,
    KPI_completed_tasks: 0,
    blockedtasksCHD_metric: 0,
    sdelano_metric: [0, 0],
    vrabote_metric: [0, 0],
    snyato_metric: [0, 0],
    kvipolneniyu_metric: [0, 0],
});

const pieChartData = reactive({
    labels: ['Выполненные', 'В работе', 'Снято', 'К выполнению'],
    datasets: [
        {
            label: 'Задачи',
            data: [0, 0, 0, 0],
            backgroundColor: ['#4caf50', '#ffc107', '#f44336', '#F555FF'],
            borderColor: ['#388e3c', '#ffa000', '#d32f2f', '#F555FF'],
            borderWidth: 1,
        },
    ],
});

const pieChartOptions = reactive({
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        tooltip: {
            callbacks: {
                label: (tooltipItem: any) => `${tooltipItem.label}: ${tooltipItem.raw}%`,
            },
        },
    },
});

// Обновление данных для графика
// Обновление данных для графика при изменении `metrix`
watch(
    () => ({
        sdelano_metric: metrix.sdelano_metric[0],
        vrabote_metric: metrix.vrabote_metric[0],
        snyato_metric: metrix.snyato_metric[0],
        kvipolneniyu_metric: metrix.kvipolneniyu_metric[0],
    }),
    (newMetrix) => {
        // Убедитесь, что метрики имеют значения
        pieChartData.datasets[0].data = [
            newMetrix.sdelano_metric ?? 0, // если данные пустые, устанавливаем 0
            newMetrix.vrabote_metric ?? 0,
            newMetrix.snyato_metric ?? 0,
            newMetrix.kvipolneniyu_metric ?? 0,
        ];
    },
    { immediate: true }, // сразу применить на начальном этапе
);
// Получение метрик
const { mutateAsync: getMetrix } = useGetMetrics();
const handleFetchMetrics = async () => {
    const response = await getMetrix({
        sprint_id: sprintID.value,
        first_date: startDate.value,
        second_date: endDate.value,
    });
    if (response) {
        // Обновляем реактивный объект `metrix`
        Object.assign(metrix, response);
    }
};

// Цвет для круга
const generateBrightPastelColor = (): string => {
    const colors = ['#FF8ACE', '#3DEABC', '#A48AFF'];
    return colors[Math.floor(Math.random() * colors.length)];
};

// Переход назад
const goToSprints = () => {
    router.push('/sprints');
};

// Загрузка данных спринта
onMounted(async () => {
    try {
        sprintID.value = Number(route.params.id);
        if (!sprintID.value) throw new Error('Invalid sprint ID');

        const response = await api.get<Sprint>(`/sprints/${sprintID.value}`);
        sprint.value = response.data;
    } catch (err: any) {
        console.error('Error fetching sprint:', err);
    }
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
    .detailPageHeader {
        display: flex;
        flex-direction: column;
        gap: 40px;
        width: 100%;
        .sprintInfo {
            display: flex;
            flex-direction: row;
            width: 100%;
            align-items: center;
            gap: 24px;
            .back {
                display: flex;
                width: 36px;
                height: 36px;
                justify-content: center;
                align-items: center;
                gap: 10px;
                border-radius: 8px;
                background: rgba(69, 163, 250, 0.1);
            }
            .name {
                display: flex;
                align-items: flex-start;
                gap: 12px;
                width: 100%;
                align-items: center;
                .circle {
                    height: 16px;
                    width: 16px;
                    border-radius: 50%;
                    flex-shrink: 0;
                }
                h2 {
                    color: var(--Base-875, #202220);
                    font-family: Inter;
                    font-size: 24px;
                    font-style: normal;
                    font-weight: 600;
                    line-height: normal;
                }
            }
        }
        .filters {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: end;
        }
    }
    .detailPageBody {
        display: flex;
        width: 100%;
        align-items: flex-start;
        align-content: flex-start;
        gap: 20px;
        flex-wrap: wrap;
        .healthMetric {
            display: flex;
            height: 280px;
            
            flex-direction: column;
            align-items: center;
            border-radius: 12px;
            background: #fafafa;
        }
        .kpiMetrics {
            display: flex;
            width: 314px;
            height: 280px;
            flex-direction: column;
            align-items: flex-start;
            gap: 20px;
            flex-shrink: 0;
            .metric {
                display: flex;
                height: 55px;
                height: 100%;
                padding: 18px 20px;
                justify-content: space-between;
                align-items: center;
                align-self: stretch;
                border-radius: 12px;
                background: #fafafa;
                p {
                    color: var(--Base-875, #202220);
                    font-family: Inter;
                    font-size: 14px;
                    font-style: normal;
                    font-weight: 500;
                    line-height: normal;
                }
                h5 {
                    width: auto;
                    height: auto;
                    min-width: 28px;
                    min-height: 28px;
                    padding: 5px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: rgba(69, 163, 250, 0.1);
                    border-radius: 8px;
                    color: #3890e3;
                    font-family: Inter;
                    font-size: 16px;
                    font-style: normal;
                    font-weight: 600;
                    line-height: normal;
                }
            }
        }
        .taskStatus {
            display: flex;
            height: 280px;
            padding: 20px;
            flex-direction: column;
            align-items: center;
            border-radius: 12px;
            background: #fafafa;
            h3 {
                color: var(--Base-875, #202220);
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 500;
                line-height: normal;
            }
        }
        .taskStatusText {
            display: flex;
            flex-direction: row;
            gap: 20px;
            .textMetric {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                gap: 10px;
                border-radius: 12px;
                background: #fafafa;
                padding: 20px;
                p {
                    color: var(--Base-875, #202220);
                    font-family: Inter;
                    font-size: 18px;
                    font-style: normal;
                    font-weight: 700;
                    line-height: normal;
                }
                h5 {
                    color: var(--Base-875, #202220);
                    font-family: Inter;
                    font-size: 16px;
                    font-style: normal;
                    font-weight: 600;
                    line-height: normal;
                }
            }
        }
    }
}
</style>
