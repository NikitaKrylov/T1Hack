<template>
    <div class="sideBar">
        <div class="topPart">
            <div class="logo">
                <CustomIcon id="logo" :width="207" :height="33" className="logo" />
            </div>
            <nav class="menu">
                <CustomMenuLink :to="`/home`" icon="home" text="Главная" />
                <CustomMenuLink :to="`/projects`" icon="projects" text="Проекты" />
                <CustomMenuLink :to="`/sprints`" icon="sprints" text="Спринты" />
                <CustomMenuLink :to="`/teams`" icon="workers" text="Команды" />
            </nav>
        </div>
        <div class="profile" @click="router.push('/profile')">
            <div class="avatar">TU</div>
            <div class="profileInfo">
                <h4>Тестовый юзер</h4>
                <p>Администратор</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import CustomIcon from '@/ui/CustomIcon.vue';
import CustomMenuLink from '@/ui/CustomMenuLink.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style lang="scss" scoped>
.sideBar {
    height: 100%;
    min-width: 240px;
    display: flex;
    box-sizing: border-box;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;

    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px;
    .topPart {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 60px;

        width: 100%;
        .menu {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 24px;
            flex-shrink: 0;
        }
    }
    .profile {
        width: 100%;
        display: flex;
        align-items: center;
        gap:12px;
        .avatar {
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #a0a2a0;
            border-radius: 50%;
        }
        .profileInfo {
            width: fit-content;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 4px;
            h4 {
                color: var(--Base-875, #202220);
                font-family: Inter;
                font-size: 14px;
                font-style: normal;
                font-weight: 600;
                line-height: normal;
                width: fit-content;
            }
            p {
                color: var(--Base-375, #a0a2a0);
                font-family: Inter;
                font-size: 12px;
                font-style: normal;
                font-weight: 400;
                line-height: normal;
                width: fit-content;
            }
        }
    }
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
