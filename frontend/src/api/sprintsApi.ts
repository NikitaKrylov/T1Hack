import { useMutation, useQuery } from '@tanstack/vue-query';
import api from './baseApi';

// UserResponse and Sprint types
type UserResponse = null;

export interface Sprint {
    id: number;
    name: string;
    user_id: number;
    sprint_status: string;
    started_at: string;
    finished_at: string;
}

// Utility function to add abort support to an API call
const postWithAbort = (url: string, body: { file: File }, signal: AbortSignal) => {
    return api
        .post(url, body, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            signal, // Pass the signal here
        })
        .then((res) => res.data);
};

// Мутация для импорта спринтов с отменой
export const useSprintsImport = () => {
    return useMutation<UserResponse, Error, { file: File, signal: AbortSignal }>({
        mutationFn: ({ file, signal }) => {
            return postWithAbort('/sprints/import', { file }, signal);
        },
    });
};

// Мутация для импорта сущностей с отменой
export const useEntitiesImport = () => {
    return useMutation<UserResponse, Error, { file: File, signal: AbortSignal }>({
        mutationFn: ({ file, signal }) => {
            return postWithAbort('/entities/import', { file }, signal);
        },
    });
};

// Мутация для импорта истории с отменой
export const useHistoryImport = () => {
    return useMutation<UserResponse, Error, { file: File, signal: AbortSignal }>({
        mutationFn: ({ file, signal }) => {
            return postWithAbort('/history/import', { file }, signal);
        },
    });
};

// Запрос на получение данных пользователя
export const useGetSprints = () => {
    return useMutation<Sprint[], Error>({
        mutationFn: () => {
            return api.post('/sprints/list').then((res) => res.data);
        },
    });
};

export const useGetSprint = (id:number) => {
    return useQuery<Sprint, Error>({
        queryKey: ['sprint', id],
        queryFn: () => api.get<Sprint>(`/sprints/${id}`).then((res) => res.data),
        enabled: !!id,
    });
};

export const useGetMetrics = () => {
    return useMutation<UserResponse, Error, { sprint_id: number, first_date: string, second_date: string }>({
        mutationFn: (body) => {
            return api.post('/metrix', body).then((res) => res.data);
        },
    });
};