<template>
    <div class="loginPage">
        <div class="modal">
            <h2>Вход в аккаунт</h2>
            <div class="inpGrp">
                <CustomInput v-model="emailValue" labelTxt="Введите почту" :errorTxt="emailValidationError" typeInp="email" placeholderTxt="Почта"  />
                <CustomInput v-model="passwordValue" labelTxt="Введите пароль" errorTxt="" typeInp="password" placeholderTxt="Пароль" />
            </div>
            <div class="toolbar">
                <div class="wrapBtn">
                    <MainButton text="Войти" type="primary" />
                    <p>{{ fetchError }}</p>
                </div>
                <p class="forgot">Забыли пароль?</p>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import CustomInput from '@/ui/CustomInput.vue';
import MainButton from '@/ui/MainButton.vue';
import { ref, watch } from 'vue';


defineOptions({
    name: 'LoginPage',
});
const fetchError = ref('');
const emailValidationError = ref('');
const emailValue = ref('');
const passwordValue = ref('');

watch(emailValue, (newEmail) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(newEmail)) {
        emailValidationError.value = 'Неправильный email';
    }
    if (newEmail === '' || emailRegex.test(newEmail)) {
        emailValidationError.value = '';
    }
    
});
watch(passwordValue, (newPassword) => {
    passwordValue.value = newPassword;
});
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

        /* Header/Header 1 */
        font-family: Inter;
        font-size: var(--font-h2, 20px);
        font-style: normal;
        font-weight: 600;
        line-height: 24px; /* 120% */
    }
    .modal {
        display: flex;
        padding: 40px 32px;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 40px;

        border-radius: 16px;
        background: var(--Base-0, #fff);
        box-shadow:
            0px 353px 99px 0px rgba(0, 0, 0, 0),
            0px 226px 90px 0px rgba(0, 0, 0, 0),
            0px 127px 76px 0px rgba(0, 0, 0, 0.02),
            0px 57px 57px 0px rgba(0, 0, 0, 0.03),
            0px 14px 31px 0px rgba(0, 0, 0, 0.03);
        .inpGrp {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 16px;
        }
    }
    .toolbar {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 16px;
        width: 100%;
        .wrapBtn {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            width: 100%;
        }
        .forgot {
            color: #333;
            font-size: 12px;
            font-style: normal;
            font-weight: 400;
            line-height: 16px; /* 133.333% */
        }
    }
}
</style>
