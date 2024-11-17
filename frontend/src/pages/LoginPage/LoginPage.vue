<template>
    <div class="loginPage">
        <div class="modal">
            <h2>Вход в аккаунт</h2>
            <div class="inpGrp">
                <CustomInput v-model="emailValue" labelTxt="Введите почту" :errorTxt="emailValidationError" typeInp="email" placeholderTxt="Почта" />
                <CustomInput v-model="passwordValue" labelTxt="Введите пароль" typeInp="password" placeholderTxt="Пароль" />
            </div>
            <div class="toolbar">
                <div class="wrapBtn">
                    <MainButton text="Войти" type="primary" :disabled="isButtonDisabled" @click="handleLogin" />
                    <p class="error">{{ fetchError }}</p>
                </div>
                <p class="forgot">Забыли пароль?</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useLoginUser } from '@/api/userApi';
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';
import { setCookie } from '@/utils/setCookie';

import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'LoginPage',
});

const emailValue = ref('');
const passwordValue = ref('');
const emailValidationError = ref('');
const fetchError = ref('');
const router = useRouter();
const { mutateAsync: loginUser } = useLoginUser();

const validateEmail = (email: string): string => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!email) return 'Email не может быть пустым';
    if (!emailRegex.test(email)) return 'Неправильный email';
    return '';
};
watch(emailValue, (newEmail) => {
    emailValidationError.value = validateEmail(newEmail);
});
// Доступность кнопки
const isButtonDisabled = computed(() => !!emailValidationError.value || !emailValue.value || !passwordValue.value);

const handleLogin = async () => {
    emailValidationError.value = validateEmail(emailValue.value);
    try {
        const response = await loginUser({ username: emailValue.value, password: passwordValue.value });
        if (response && response.access_token) {
            setCookie('token', response.access_token, 12);
            fetchError.value = '';
            router.push('/sprints');
        }
    } catch (error: any) {
        fetchError.value = error?.response?.data?.detail || 'Произошла ошибка при входе';
    }
};
</script>

<style lang="scss" scoped>
.loginPage {
    width: 100%;
    height: 100dvh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: var(--font-main, 'Inter');

    h2 {
        color: var(--Base-hack-800, #333);
        font-family: Inter;
        font-size: var(--font-h2, 20px);
        font-weight: 600;
        line-height: 24px;
    }

    .modal {
        display: flex;
        flex-direction: column;
        padding: 40px 32px;
        align-items: center;
        gap: 40px;
        border-radius: 16px;
        background: var(--Base-0, #fff);
        box-shadow: 0px 14px 31px rgba(0, 0, 0, 0.03);

        .inpGrp {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
    }

    .toolbar {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        width: 100%;

        .wrapBtn {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            width: 100%;

            .error {
                color: red;
                font-size: 14px;
            }
        }

        .forgot {
            color: #333;
            font-size: 12px;
            font-weight: 400;
        }
    }
}
</style>
