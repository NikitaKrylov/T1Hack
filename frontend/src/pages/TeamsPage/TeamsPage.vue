<template>
    <main class="teamsPage">
        <h3>Команды</h3>
        <div class="teams">
            <TeamComponent name="Пылающий легион" teammates="32" sprintsCount="64" />
        </div>
    </main>
</template>
<script setup lang="ts">
import TeamComponent from '@/components/TeamComponent.vue';

defineOptions({
    name: 'TeamsPage',
});
</script>
<style lang="scss" scoped>
.teamsPage {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 40px 60px 640px 40px;
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    border-radius: 16px;
    background: var(--White-100, #fff);
    h3 {
        color: var(--Base-875, #202220);
        font-family: Inter;
        font-size: 24px;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
}
</style>
