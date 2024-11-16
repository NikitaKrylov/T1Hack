<template>
    <div class="addSprintPage">
        <div class="addSprint"></div>
        <div class="vp"></div>
    </div>
</template>
<script setup lang="ts">
defineOptions({
    name: 'AddSprintPage',
});
</script>
<style lang="scss">
.addSprintPage {
    display: flex;
    height: 100%;
    width: 100%;
    flex-direction: row;
    gap: 20px;
    .addSprint {
        display: flex;
        min-width: 548px;
        max-width: 588px;
        height: 100%;
        padding: 40px;
        flex-direction: column;
        align-items: flex-start;
        gap: 52px;
        border-radius: 16px;
        background: var(--White-100, #fff);
    }
    .vp{
        display: flex;
        width: 400px;
        height: 100%;
        padding: 40px;
        flex-direction: column;
        align-items: flex-start;
        gap: 52px;
        border-radius: 16px;
        background: var(--White-100, #fff);
    }
}
</style>
