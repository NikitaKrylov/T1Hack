<template>
    <main class="addSprintPage">
        <div class="addSprint">
            <div class="addSprintHeader">
                <button class="back" @click="goToSprints"><CustomIcon id="arrow_back" :width="16" :height="16" /></button>
                <h2>Загрузка спринта(ов)</h2>
            </div>
            <div class="addSprintBody">
                <AddSprintComponent
                    number="1"
                    text1="Информация о спринте"
                    text2="Загрузите файл с информацией об одном или нескольких спринтах"
                    :state="state1"
                    v-model="file1"
                />
                <AddSprintComponent
                    number="2"
                    text1="Информация о задачах"
                    text2="Загрузите файл, который содержит информацию по задачам"
                    :state="state2"
                    v-model="file2"
                />
                <AddSprintComponent
                    number="3"
                    text1="Данные об изменение задач"
                    text2="Загрузите файл с информацией об изменение задач"
                    :state="state3"
                    v-model="file3"
                />
            </div>
            <div class="bottom" v-if="state1 === 'done' && state2 === 'done' && state3 === 'done'">
                <MainButton type="primary" text="Загрузить файлы" style="width: 412px" size="l" @click="handleSendFiles" v-if="!isLoading" />
                <MainButton type="secondary" text="Отмена загрузки" style="width: 412px" size="l" @click="stopSendFiles" v-else />
            </div>
        </div>

        <div class="vp">
            <img src="/img/rightC.svg" />
        </div>
    </main>
</template>
<script setup lang="ts">
import { useEntitiesImport, useHistoryImport, useSprintsImport } from '@/api/sprintsApi';
import AddSprintComponent from '@/components/AddSprintComponent.vue';
import CustomIcon from '@/ui/CustomIcon.vue';
import MainButton from '@/ui/MainButton.vue';
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'AddSprintPage',
});

type State = 'done' | 'active' | 'disabled';

const router = useRouter();

const { mutateAsync: importHistory } = useHistoryImport();
const { mutateAsync: importEntities } = useEntitiesImport();
const { mutateAsync: importSprints } = useSprintsImport();

const isLoading = ref(false);
const file1 = ref<File | null>(null);
const file2 = ref<File | null>(null);
const file3 = ref<File | null>(null);

const state1 = ref<State>('active');
const state2 = ref<State>('disabled');
const state3 = ref<State>('disabled');

// Cancellation controllers
const controller1 = new AbortController();
const controller2 = new AbortController();
const controller3 = new AbortController();

watch(file1, (newValue) => {
    if (newValue) {
        state1.value = 'done';
        state2.value = 'active';
    } else {
        state1.value = 'active';
        state2.value = 'disabled';
    }
});

watch(file2, (newValue) => {
    if (newValue) {
        state2.value = 'done';
        state3.value = 'active';
    } else {
        state2.value = 'active';
        state3.value = 'disabled';
    }
});

watch(file3, (newValue) => {
    if (newValue) {
        state3.value = 'done';
    } else {
        state3.value = 'active';
    }
});

const goToSprints = () => {
    router.push('/sprints');
};

const handleSendFiles = async () => {
    try {
        if (file1.value && file2.value && file3.value) {
            isLoading.value = true; // Start loading
            console.log("dsa");
            
            // Make sure each mutation has the appropriate AbortController signal
            const sprintResponse = await importSprints({ file: file1.value, signal: controller1.signal });
            console.log('Sprint import success', sprintResponse);

            const entitiesResponse = await importEntities({ file: file2.value, signal: controller2.signal });
            console.log('Entities import success', entitiesResponse);

            const historyResponse = await importHistory({ file: file3.value, signal: controller3.signal });
            console.log('History import success', historyResponse);

            goToSprints();
            isLoading.value = false; // Finish loading
        }
    } catch (error: unknown) {
        // TypeScript assertion to tell the compiler that error is of type Error
        if ((error as Error).name === 'AbortError') {
            console.log('Upload was canceled');
        } else {
            console.error('Ошибка при загрузке файлов:', error);
        }
        isLoading.value = false; // Finish loading on error or cancellation
    }
};

const stopSendFiles = () => {
    isLoading.value = false; // Stop loading
    // Reset states to initial values
    state1.value = 'active';
    state2.value = 'disabled';
    state3.value = 'disabled';
    // Cancel ongoing mutations if they are running
    controller1.abort();
    controller2.abort();
    controller3.abort();

    // Optionally clear the files if you want to reset the process
    file1.value = null;
    file2.value = null;
    file3.value = null;

    console.log('File upload stopped and mutations cancelled');
};
</script>

<style lang="scss" scoped>
.addSprintPage {
    display: flex;
    height: 100%;
    width: 100%;
    flex-direction: row;
    gap: 20px;
    .addSprint {
        position: relative;
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
        .addSprintHeader {
            display: flex;
            align-items: center;
            gap: 16px;
            h2 {
                width: fit-content;
                color: var(--Base-875, #202220);
                font-family: Inter;
                font-size: 24px;
                font-style: normal;
                font-weight: 600;
                line-height: normal;
            }
            .back {
                display: flex;
                width: 36px;
                height: 36px;
                justify-content: center;
                align-items: center;
                gap: 10px;
                border-radius: 8px;
                background: rgba(69, 163, 250, 0.1);
            }
        }
        .addSprintBody {
            display: flex;
            width: 460px;
            flex-direction: column;
            align-items: flex-start;
            gap: 40px;
            overflow: auto;
        }
        .bottom {
            position: absolute;
            bottom: 40px;
            right: 40px;
            display: flex;
            justify-content: end;
            align-items: center;
        }
    }
    .vp {
        display: flex;
        width: 100%;
        height: 100%;
        padding: 40px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 52px;
        border-radius: 16px;
        background: var(--White-100, #fff);
        img{
            width: auto;
            height: 100%;
        }
    }
}
</style>
