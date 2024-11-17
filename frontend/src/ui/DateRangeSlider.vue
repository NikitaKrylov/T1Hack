<template>
    <div class="range-slider">
        <label>Исследуемый период</label>
        <!-- Отображение значений -->
        <div class="range-values-wrapper">
            <div class="range-values">
                <span>{{ formatDate(sliderMinValue) }}</span>
                <span>{{ formatDate(sliderMaxValue) }}</span>
            </div>
            <div class="slider-container" ref="slider">
                <!-- Первый ползунок -->
                <input type="range" class="thumb thumb-min" :min="0" :max="totalDays" :step="1" v-model.number="sliderMinValue" />
                <!-- Второй ползунок -->
                <input type="range" class="thumb thumb-max" :min="0" :max="totalDays" :step="1" v-model.number="sliderMaxValue" />
                <!-- Прогресс между двумя ползунками -->
                <div class="range-progress" :style="{ left: `${getPercent(sliderMinValue)}%`, right: `${100 - getPercent(sliderMaxValue)}%` }"></div>
                <div class="range" style="left: 0; right: 100%"></div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

// Пропсы компонента
const { endDateInput, startDateInput } = defineProps<{
    endDateInput: string | Date;
    startDateInput: string | Date;
}>();
const emit = defineEmits(['update:startDate', 'update:endDate']);

const parsedStartDate = computed(() => (typeof startDateInput === 'string' ? new Date(startDateInput) : startDateInput));
const parsedEndDate = computed(() => (typeof endDateInput === 'string' ? new Date(endDateInput) : endDateInput));
// Вычисление общего количества дней в диапазоне
const totalDays = computed(() => Math.ceil((parsedEndDate.value.getTime() - parsedStartDate.value.getTime()) / (1000 * 60 * 60 * 24)));

// Ползунки (числовые значения от 0 до totalDays)
const sliderMinValue = ref(0); // Начальное значение (0 = стартовая дата)
const sliderMaxValue = ref(totalDays.value); // Конечное значение (totalDays = последняя дата)

// Функция преобразования числа в дату
const formatDate = (value: number) => {
    const date = new Date(startDateInput);
    date.setDate(parsedStartDate.value.getDate() + value);
    return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
};
const formatDateToYMD = (value: number) => {
    const date = new Date(startDateInput);
    date.setDate(parsedStartDate.value.getDate() + value);
    return date.toISOString().split('T')[0];
};
watch(sliderMinValue, (newMinValue) => {
    emit('update:startDate', formatDateToYMD(newMinValue));
});
watch(sliderMaxValue, (newMaxValue) => {
    emit('update:endDate', formatDateToYMD(newMaxValue));
});
// Вычисление процента для позиции ползунков
const getPercent = (value: number) => {
    return (value / totalDays.value) * 100;
};

// Обновление значений, если пропсы изменятся
watch(
    () => [startDateInput, endDateInput],
    () => {
        sliderMinValue.value = 0;
        sliderMaxValue.value = totalDays.value;
    },
);
</script>

<style lang="scss" scoped>
.range-slider {
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 293px;
    label {
        color: var(--Base-750, #404240);
        font-family: Inter;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: normal;
    }
}
.range-values-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
}
.slider-container {
    position: relative;
    height: auto;
    display: flex;
    align-items: center;
    width: 100%;
}

input[type='range'] {
    position: absolute;
    width: 100%;
    height: 8px;
    appearance: none;
    -webkit-appearance: none;
    background: transparent;
    pointer-events: none; /* Запретить прямое взаимодействие с полосой */
}

input[type='range']::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: rgba(69, 163, 250, 1);
    cursor: pointer;
    pointer-events: auto; /* Разрешить взаимодействие с ползунком */
    z-index: 3;
}

input[type='range']::-moz-range-thumb {
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: rgba(69, 163, 250, 1);
    cursor: pointer;
    z-index: 2;
}

input[type='range']:focus {
    outline: none;
}

.range-progress {
    position: absolute;
    height: 8px;
    background: rgba(69, 163, 250, 1);
    border-radius: 4px;
    pointer-events: none;
    z-index: 3; /* Запретить взаимодействие с полосой прогресса */
}
.range {
    position: absolute;
    height: 8px;
    background: #a9d9f6;
    border-radius: 4px;
    pointer-events: none;
    width: 100%;
    z-index: 0;
}
.range-values {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    border-radius: 8px;
    background: rgba(69, 163, 250, 0.1);
    height: 48px;
    padding: 16px 40px;
    span {
        color: var(--Base-875, #202220);
        font-family: Inter;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: normal;
    }
}
</style>
