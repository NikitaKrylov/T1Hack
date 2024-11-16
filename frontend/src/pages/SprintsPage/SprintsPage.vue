<template>
    <main class="sprintsPage">Sprints Page</main>
</template>
<script setup lang="ts">
defineOptions({
    name: 'SprintsPage',
});
</script>
<style lang="scss">
.sprintsPage {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 40px 60px 640px 40px;
    flex-direction: column;
    align-items: flex-start;
    gap: 32px;
    border-radius: 16px;
    background: var(--White-100, #fff);
}
</style>
