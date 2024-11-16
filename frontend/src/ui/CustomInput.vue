<template>
    <div class="custom-input">
        <label>{{ labelTxt }}</label>
        <div class="inpWrapper">
            <input :type="currentType" :placeholder="placeholderTxt" v-model="modelValue" :value="modelValue" />
            <CustomIcon v-if="typeInp === 'password'" id="eye" :width="24" :height="24" @click="isPasswordVisible ? hidePassword() : showPassword()" style="justify-self: end" />
        </div>
        <small v-if="errorTxt" role="alert" class="error-message">{{ errorTxt }}</small>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import CustomIcon from './CustomIcon.vue';
defineOptions({
    name: 'InputComp',
});

const props = withDefaults(
    defineProps<{
        labelTxt?: string;
        typeInp?: string;
        modelValue?: string;
        errorTxt?: string;
        placeholderTxt?: string;
    }>(),
    {
        labelTxt: '',
        typeInp: 'text',
        errorTxt: '',
    },
);
const emit = defineEmits(['update:modelValue']);

const modelValue = defineModel();
const text = ref('');
const isPasswordVisible = ref(false);
const currentType = computed(() => {
    return isPasswordVisible.value ? 'text' : props.typeInp;
});

// Methods to show/hide password
const showPassword = () => {
    isPasswordVisible.value = true;
};

const hidePassword = () => {
    isPasswordVisible.value = false;
};
</script>

<style scoped lang="scss">
.custom-input {
    display: flex;
    max-width: 300px;
    width: 100%;
    min-width: 116px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;

    label {
        color: #767676;

        /* text-tiny */
        font-family: Inter;
        font-size: 12px;
        font-style: normal;
        font-weight: 400;
        line-height: 16px; /* 133.333% */
    }
    .inpWrapper {
        display: flex;
        height: 40px;
        padding: 12px 16px;
        align-items: center;
        gap: 12px;
        align-self: stretch;
        border-radius: 8px;
        border: 1px solid var(--Base-hack-200, #ccc);
        background: var(--Base-hack-0, #fff);
        input {
            width: 100%;
            height: 100%;
            color: var(--Base-hack-800, #333);
            font-family: Inter;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 114.286% */
        }
        input::placeholder {
            color: var(--Base-hack-300, #b2b2b2);
            font-family: Inter;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 114.286% */
        }
    }
    small {
        color: var(--Additional-Error-500, #ea4e3d);
        font-feature-settings:
            'liga' off,
            'clig' off;
        font-family: Inter;
        font-size: 12px;
        font-style: normal;
        font-weight: 500;
        line-height: 12px; /* 100% */
    }
}
</style>
