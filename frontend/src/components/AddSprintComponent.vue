<template>
    <div class="addSprintComponent">
        <div :class="{ number: true, 'is-disabled': state === 'disabled', 'is-done': state === 'done' }">{{ props.number }}</div>
        <div class="add">
            <div :class="{ info: true, 'is-disabled': state === 'disabled' }">
                <h4>{{ props.text1 }}</h4>
                <p>{{ props.text2 }}</p>
            </div>
            <DropZone v-model="file" @file-selected="handleSelectFile" :state="state" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, defineEmits } from 'vue';
import DropZone from './DropZone.vue';

defineOptions({ name: 'AddSprintComponent' });

const emit = defineEmits<{
    (e: 'update:modelValue', file: File | null): void;
}>();

const props = defineProps<{
    number: string;
    state: 'active' | 'disabled' | 'done';
    text1: string;
    text2: string;
    modelValue: File | null;
}>();
const file = ref<File | null>(props.modelValue);
watch(
    () => file.value,
    (newValue) => {
        emit('update:modelValue', newValue); // Обновляем значение на родителе
    },
);

watch(
    () => props.modelValue,
    (newValue) => {
        file.value = newValue;
    },
);

watch(
    () => file.value,
    (newValue) => {
        emit('update:modelValue', newValue); // Синхронизация с родителем
    },
);
const handleSelectFile = (files: FileList, fileName: string) => {
    file.value = files[0];
};
</script>
<style lang="scss" scoped>
.addSprintComponent {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    width: 100%;
    .number {
        display: flex;
        width: 32px;
        height: 32px;
        flex-shrink: 0;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-radius: 8px;
        background: rgba(69, 163, 250, 0.1);

        color: #3890e3;
        font-family: Inter;
        font-size: 16px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
        &.is-disabled {
            color: #c0c2c0;
            background-color: #F0F2F0;
        }
        &.is-done {
            color: #88E079;
            background-color: rgba(151, 231, 138, 0.20);
        }
    }
    .add {
        display: flex;
        width: 412px;
        flex-direction: column;
        align-items: flex-start;
        gap: 24px;
        .info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
            align-self: stretch;
            &.is-disabled {
                h4 {
                    color: #c0c2c0;
                }
                p {
                    color: #c0c2c0;
                }
            }
            h4 {
                color: var(--Base-875, #202220);
                font-family: Inter;
                font-size: 20px;
                font-style: normal;
                font-weight: 500;
                line-height: normal;
            }
            p {
                color: var(--Base-500, #808280);
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 400;
                line-height: normal;
            }
        }
    }
}
</style>
