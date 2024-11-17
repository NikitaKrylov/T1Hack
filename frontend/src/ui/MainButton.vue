<template>
    <button :class="buttonClass">
        <p v-if="text">{{ text }}</p>
        <CustomIcon v-if="icon" :id="icon" :width="16" :height="16"/>
    </button>
</template>

<script setup lang="ts">
defineOptions({
    name: 'MainButton',
});
import { computed } from 'vue';
import CustomIcon from './CustomIcon.vue';

const { type = 'primary', size = 'l' } = defineProps<{ text?: string; type?: 'primary' | 'secondary' | 'third'; size?: 's' | 'm' | 'l'; icon?: string  }>();

const buttonClass = computed(() => ['btn', { 'btn--primary': type === 'primary' }, { 'btn--secondary': type === 'secondary' }, {'btn--third': type === 'third'}, { 'btn--small': size === 's', 'btn--medium': size === 'm', 'btn--large': size === 'l' }]);

</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    width: 320px;
    padding: 15px 20px;
    justify-content: center;
    align-items: center;
    gap: 8px;
    border-radius: 8px;
    background-color: #45a3fa;
    transition: all 0.5s;

    color: var(--color-base-0, #fff);
    text-align: center;
    font-family: var(--font-main, 'Inter');
    font-size: 14px;
    font-style: normal;
    font-weight: 500;
    line-height: 18px;
    transition: background-color 0.3s, color 0.3s, border-color 0.3s;
    &--primary {
        background-color: #45a3fa;
        color: var(--Base-hack-0, #fff);
        &:hover {
            background-color: #3890e3;
        }
    }

    &--secondary {
        border: 1px solid #45A3FA;
        background-color: transparent;
        color: #45A3FA;
        &:hover {
            color: var(--color-base-0, #fff);
            border: 1px solid #45A3FA;
            background-color: #45A3FA;
        }
    }
    &--third {
        color:rgba(56, 144, 227, 1);
        background-color: rgba(69, 163, 250, 0.1);

        &:hover {
            background-color: rgba(69, 163, 250, 0.25);

        }
    }
    // Размеры кнопки.
    &--small {
        height: 24px;
        padding: 3px 0px;
        font-size: 14px;
        line-height: 18px;
    }

    &--medium {
        height: 32px;
        padding: 7px 0px;
        font-size: 14px;
        line-height: 18px;
    }

    &--large {
        height: 40px;
        padding: 12px 0px;
        font-size: 14px;
        line-height: 18px;
    }

    p {
        z-index: 2;
        width: fit-content;
    }
}

</style>
