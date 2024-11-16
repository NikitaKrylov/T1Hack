<template>
    <router-link :to="to" :class="['link', isActive && 'active']" v-bind="filteredProps">
        <CustomIcon :class="icon" :id="icon" :width="32" :height="32" />
        <span class="text">{{ text }}</span>
    </router-link>
</template>

<script setup lang="ts">
import { computed, defineProps, toRefs } from 'vue';
import { useRoute } from 'vue-router';
import CustomIcon from '@/ui/CustomIcon.vue';

interface LinkProps {
    icon: string;
    text?: string;
    to: string;
}

const props = defineProps<LinkProps>();
const { to, icon, text } = toRefs(props);

const filteredProps = computed(() => {
    const { to, icon, text, ...rest } = props; // Exclude `to`, `icon`, and `text` from `props`
    return rest;
});

// Check if the current route matches the link's target
const route = useRoute();
const isActive = computed(() => route.path.includes(to.value));
</script>

<style scoped lang="scss">
.link {
    width: 100%;
    display: flex;
    flex-direction: row;
    padding: 12px 16px;
    align-items: center;
    gap: 12px;
    border-radius: 12px;

    user-select: none;
    outline: none;
    color: var(--color-base-875, #202220);
    --webkit-tap-highlight-color: transparent;
    --webkit-user-select: none;
    --moz-user-select: none;
    --ms-user-select: none;
    --o-user-select: none;
    --user-select: none;
    cursor: pointer;
    // &:focus,
    // &:active {
    //     background-color: transparent;
    //     outline: none;
    // }

    .icon {
        display: block;
        transition: color 0.2s ease; /* Transition for color changes */
        /* Ensure icon inherits color from the link */
        color: inherit; /* This ensures the icon uses the link's color */
    }
}
.text {
    color: var(--color-base-875, #202220);
    font-family: Inter;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
}
.active {
    color: var(--color-base-0, #fff); /* Active link color */
    background: #45a3fa;
    .text{
        color: var(--color-base-0, #fff); /* Active link color */
    }
}
</style>
