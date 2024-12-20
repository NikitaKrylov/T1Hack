import { createApp } from 'vue';
import App from './App.vue';
import { createWebHistory, createRouter } from 'vue-router';
import queryClient from './api/queryClient';
import { createPinia } from 'pinia';
import HighchartsVue from 'highcharts-vue'
import MainLayout from './layouts/MainLayout.vue';
import ErrorPage from './pages/ErrorPage.vue';

import AiChatPage from './pages/AiChatPage/AiChatPage.vue';
import SettingsPage from './pages/SettingsPage/SettingsPage.vue';
import LoginPage from './pages/LoginPage/LoginPage.vue';
import TeamsPage from './pages/TeamsPage/TeamsPage.vue';
import { VueQueryPlugin } from '@tanstack/vue-query';
import SprintsPage from './pages/SprintsPage/SprintsPage.vue';
import path from 'path';
import AddSprintPage from './pages/SprintsPage/AddSprintPage.vue';
import DetailSprintPage from './pages/SprintsPage/DetailSprintPage.vue';

const routes = [
    { path: '/:catchAll(.*)', component: ErrorPage },
    { path: '/login', component: LoginPage },
    {
        path: '/teams',
        component: MainLayout,
        children: [{ path: '', component: TeamsPage }],
    },
    { path: '/sprints', component: MainLayout, children: [{ path: '', component: SprintsPage }] },
    { path: '/sprints/add', component: MainLayout, children: [{ path: '', component: AddSprintPage }] },
    { path: '/sprints/:id', component: MainLayout, children: [{ path: '', component: DetailSprintPage }] },
   
    // { path: '/ai_chat', component: MainLayout, children: [{ path: '', component: AiChatPage }] },
    // { path: '/settings', component: MainLayout, children: [{ path: '', component: SettingsPage }] },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});
// router.beforeEach((to, from, next) => {
//     const roleStore = useRoleStore();
//     const userRole = roleStore.role;

//     // Разрешаем доступ для всех пользователей на страницы логина и регистрации
//     const publicPaths = ['/login/patient', '/register/patient', '/login/doctor', '/register/doctor'];
//     if (publicPaths.includes(to.path)) {
//         return next();
//     }

//     // Проверка доступа для маршрутов пациентов и докторов
//     if (to.path.includes('/patient') && userRole !== 'patient') {
//         return next('/error');
//     } else if (to.path.includes('/doctor') && userRole !== 'doctor') {
//         console.log(to.path.includes('/doctor'));

//         return next('/error');
//     }

//     next(); // Разрешаем доступ, если проверка пройдена
// });
const pinia = createPinia();

createApp(App).use(HighchartsVue).use(pinia).use(VueQueryPlugin, { queryClient }).use(router).mount('#app');
