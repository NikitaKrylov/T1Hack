<template>
    <button :class="buttonClass">
        <p>{{ text }}</p>
    </button>
</template>

<script setup lang="ts">
defineOptions({
    name: 'MainButton',
});
import { computed } from 'vue';

const { type = 'primary' } = defineProps<{ text: string; type?: 'primary' | 'secondary' }>();

const buttonClass = computed(() => ['btn', { 'btn--secondary': type === 'secondary' }]);
</script>

<style lang="scss">
.btn {
    display: flex;
    width: 320px;
    padding: 15px 20px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    border-radius: 8px;
    background: #45a3fa;
    transition: all 0.5s;

    color: var(--color-base-0, #fff);
    text-align: center;
    font-family: Inter;
    font-size: 14px;
    font-style: normal;
    font-weight: 600;
    line-height: 18px; /* 128.571% */

    &--secondary {
        border: 1px solid var(--secondary-color, #ff577b);
        background-color: var(--secondary-color, #ff577b);
        &:active {
            color: var(--secondary-color, #ff577b);
            border: 1px solid var(--secondary-color, #ff577b);
        }
    }
    &:active {
        color: var(--Base-hack-0, #fff);
        background: #3890e3;
    }
    p {
        z-index: 2;
    }
}
</style>
