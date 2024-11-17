<template>
    <div class="date-range-picker">
        <label class="title">Исследуемый период <span class="info">?</span></label>
        <div class="slider-container">
            
            <div class="range-display">
                <span>{{ formatDate(start) }}</span>
                <span>{{ formatDate(end) }}</span>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';

const min = 0; // Начало диапазона (можно задать, например, 1 ноября)
const max = 30; // Конец диапазона (например, 30 дней)

const start = ref(5); // Значение начальной даты
const end = ref(20); // Значение конечной даты

// Преобразование числа в дату
const baseDate = new Date(2023, 10, 1); // Базовая дата (1 ноября)
const formatDate = (value: number) => {
    const date = new Date(baseDate);
    date.setDate(baseDate.getDate() + value);
    return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
};

// Обновление диапазона
const updateRange = () => {
    if (start.value > end.value) {
        [start.value, end.value] = [end.value, start.value]; // Меняем местами, если нужно
    }
};
</script>
<style scoped>
.date-range-picker {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.title {
    font-size: 16px;
    font-weight: 500;
}

.slider-container {
    position: relative;
    padding: 20px;
    background: #f0f8ff;
    border: 2px solid #87cefa;
    border-radius: 8px;
}

.slider {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
    pointer-events: auto;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    background-color: #87cefa;
    border-radius: 50%;
    cursor: pointer;
}

.range-display {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    font-size: 16px;
    font-weight: 500;
    color: #000;
}
</style>
