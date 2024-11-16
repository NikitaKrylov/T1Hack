import { createApp } from 'vue';
import App from './App.vue';
import { createWebHistory, createRouter } from 'vue-router';

import GlobalAuth from './pages/GlobalAuth.vue';
import { createPinia } from 'pinia';

import MainLayout from './layouts/MainLayout.vue';
import MainPatientPage from './pages/PatientFlow/MainPatientPage.vue';
import ErrorPage from './pages/ErrorPage.vue';
import AllChatsPage from './pages/ChatsPage/AllChatsPage.vue';
import ChatPage from './pages/ChatsPage/ChatPage.vue';
import FolderPage from './pages/PatientFlow/FolderPage/FolderPage.vue';
import HistoryPage from './pages/PatientFlow/HistoryPage/HistoryPage.vue';
import AiChatPage from './pages/AiChatPage/AiChatPage.vue';
import SettingsPage from './pages/SettingsPage/SettingsPage.vue';
import ScanReportPage from './pages/ScanReportPage/ScanReportPage.vue';
import AllDoctorsPage from './pages/PatientFlow/AllDoctorsPage/AllDoctorsPage.vue';
import path from 'path';
import LoginPage from './pages/LoginPage/LoginPage.vue';

const routes = [
    // {
    //     path: '/login',
    //     component: FormLayout,
    //     children: [{ path: '', component: GlobalAuth }],
    // },
    // {
    //     path: '/patient/home',
    //     component: MainLayout,
    //     children: [{ path: '', component: MainPatientPage }],
    // },
    { path: '/:catchAll(.*)', component: ErrorPage },
    { path: '/patient/chats', component: MainLayout, children: [{ path: '', component: AllChatsPage }] },
    { path: '/doctor/chats', component: MainLayout, children: [{ path: '', component: AllChatsPage }] },
    { path: '/chat/:id', component: ChatPage },
    {
        path: '/patient/folder/:id',
        name: 'FolderPage',
        component: MainLayout,
        children: [{ path: '', component: FolderPage }],
    },
    { path: '/patient/history', component: MainLayout, children: [{ path: '', component: HistoryPage }] },
    { path: '/ai_chat', component: MainLayout, children: [{ path: '', component: AiChatPage }] }, 
    { path: '/settings', component: MainLayout, children: [{ path: '', component: SettingsPage }] },
    { path: '/scanReport', component: ScanReportPage },
    { path: '/allDoctors', component: AllDoctorsPage },
    { path: '/login', component: LoginPage}
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

createApp(App).use(pinia).use(router).mount('#app');
