import { useQuery, useMutation } from '@tanstack/vue-query';
import api from './baseApi';
import queryClient from './queryClient';

interface UserData {
    access_token:string
}

type UserResponse = UserData;

// Мутация для логина пользователя
export const useLoginUser = () => {
    return useMutation<UserResponse, Error, { username: string; password: string }>({
      mutationFn: (body) => {
        return api.post('/users/login', body, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Adjust the Content-Type if needed
          },
        }).then((res) => res.data);
      },
    });
  };

// Запрос на получение данных пользователя
export const useGetUser = () => {
    return useQuery<UserResponse, Error>({
        queryKey: ['user'],
        queryFn: () => api.get<UserResponse>('/user/get_me').then((res) => res.data),
    });
};
