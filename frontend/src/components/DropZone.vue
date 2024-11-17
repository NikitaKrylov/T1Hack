<template>
    <div
        v-if="!selectedFileName"
        class="drop-zone"
        @dragover.prevent="handleDragOver"
        @dragleave="handleDragLeave"
        @drop.prevent="handleDrop"
        :class="{ 'is-dragging': isDragging, 'is-disabled': props.state === 'disabled' }"
    >
        <p>Перетащите файлы или выберите на компьютере .csv</p>
        <MainButton
            text="Выбрать файл"
            type="third"
            @click="selectFile"
            :style="buttonStyle"
        />
        <input type="file" ref="fileInput" @change="handleFileChange" hidden accept=".csv" :disabled="state === 'disabled'" />
    </div>
    <div class="upload" v-if="selectedFileName">
        <div class="inner">
            <div class="field">
                <div class="file">
                    <CustomIcon id="markDone" :width="16" :height="16" />
                    <p>{{ selectedFileName }}</p>
                </div>
                <CustomIcon id="trash" :width="16" :height="16" @click="clearFile" style="cursor: pointer;" />
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import CustomIcon from '@/ui/CustomIcon.vue';
import MainButton from '@/ui/MainButton.vue';
import { ref, defineEmits, watch, computed } from 'vue';

const emit = defineEmits<{
    (e: 'file-selected', files: FileList, fileName: string): void;
    (e: 'update:modelValue', file: File | null): void;
}>();
const props = defineProps<{
    modelValue?: File | null;
    state: 'active' | 'disabled' | 'done';
}>();
const isDragging = ref<boolean>(false);
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFileName = ref<string | null>(props.modelValue?.name || null);
const buttonStyle = computed(() => {
    if (props.state === 'disabled') {
        return {
            background: '#F0F2F0',
            cursor: 'not-allowed',
            color: '#A0A2A0',
        };
    } else {
        return {
            background: 'rgba(69, 163, 250, 0.10)',
            cursor: 'pointer',
            color: '#45A3FA',
        };
    }
});
watch(
    () => props.modelValue,
    (newValue) => {
        selectedFileName.value = newValue?.name || null;
    },
);
const handleDragOver = () => {
    isDragging.value = true;
};

const handleDragLeave = () => {
    isDragging.value = false;
};

const handleDrop = (event: DragEvent) => {
    const files = event.dataTransfer?.files;
    if (files && files.length) {
        handleFiles(files);
    }
    isDragging.value = false;
};

const selectFile = () => {
    fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const files = target.files;
    if (files && files.length) {
        handleFiles(files);
    }
};

const handleFiles = (files: FileList) => {
    const file = files[0];
    selectedFileName.value = file.name;
    emit('update:modelValue', file);
    emit('file-selected', files, file.name);
};

const clearFile = () => {
    selectedFileName.value = null;
    if (fileInput.value) {
        fileInput.value.value = '';
    } else {
        console.error('fileInput is not available.');
    }
    emit('update:modelValue', null);
};
</script>
<style lang="scss" scoped>
.drop-zone {
    display: flex;
    width: 412px;
    padding: 24px 20px 20px 20px;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    border-radius: 16px;
    border: 1px dashed #45a3fa;
    background-color: var(--White-100, #fff);
    transition: background-color 0.3s;

    p {
        color: var(--Base-375, #a0a2a0);
        text-align: center;
        font-family: Inter;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 130%; /* 18.2px */
    }
    &.is-disabled {
        border-color: #E0E2E0;
        pointer-events: none;

        p {
            color: #C0C2C0;
        }
    }
}
.upload {
    display: flex;
    width: 412px;
    padding: 24px 20px 20px 20px;
    flex-direction: column;
    align-items: center;
    gap: 28px;
    border-radius: 16px;
    border: 1px solid #97e78a;
    background: var(--White-100, #fff);
    .inner {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        align-self: stretch;
        .field {
            display: flex;
            height: 52px;
            padding: 19px 16px;
            align-items: center;
            gap: 16px;
            align-self: stretch;
            border-radius: 16px;
            border: 1px solid var(--Base-60, #f0f2f0);
            .file {
                display: flex;
                align-items: center;
                gap: 12px;
                flex: 1 0 0;
                p {
                    color: var(--Base-875, #202220);
                    font-family: Inter;
                    font-size: 14px;
                    font-style: normal;
                    font-weight: 500;
                    line-height: normal;
                }
            }
        }
    }
}

.drop-zone.is-dragging {
    background-color: #f0f8ff;
}
</style>
