<template>
    <div class="donut-chart">
      <div class="donut" :style="donutStyle">
        <span class="percentage">{{ percentage }}%</span>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  
  // Пропс для передачи процента
  const props = defineProps<{
    percentage: number; // Процент, который нужно отобразить
  }>();
  
  // Рассчитываем стили для CSS переменных
  const donutStyle = computed(() => ({
    '--percentage': props.percentage, // Передаем процент для визуализации
  }));
  </script>
  
  <style scoped>
  .donut-chart {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 100px;
  }
  
  .donut {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(
      #4caf50 calc(var(--percentage) * 1%), /* Закрашиваемая часть */
      #e0e0e0 0% /* Оставшаяся часть */
    );
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }
  
  .donut::before {
    content: '';
    position: absolute;
    width: 70%;
    height: 70%;
    background: #fff;
    border-radius: 50%;
  }
  
  .percentage {
    font-size: 16px;
    font-weight: bold;
    color: #4caf50;
    z-index: 1;
  }
  </style>
  