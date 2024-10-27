// Or from '@reduxjs/toolkit/query' if not using the auto-generated hooks
'use client'
import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import {logout, setCredentials} from './api/apiSlice';
import {RootState} from "@/shared/providers/store/store";

interface RefreshResponse {
    access_token: string;
}

const baseQuery = fetchBaseQuery({
    baseUrl: 'http://31.129.50.189:8000', // URL вашего API
    credentials: 'include', // позволяет отправлять куки с запросом
    prepareHeaders: (headers, {getState}) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            headers.set('Authorization', `Bearer ${token}`);

        }

        return headers;
    },
});

const refreshBaseQuery = fetchBaseQuery({
    baseUrl: 'http://31.129.50.189:8001', // Указываем другой порт для обновления токена
    credentials: 'include',
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions);

    if (result.error && (result.error.status === 401)) {

        const refresh_token = localStorage.getItem('refresh_token')

        // Попытка обновить токен
        const refreshResult = await refreshBaseQuery(
            {
                url: '/refresh',
                method: 'POST',
                body: refresh_token,
                credentials: 'include',
            },
            api,
            extraOptions
        );

        if (refreshResult.data) {
            const {access_token} = refreshResult.data as RefreshResponse
            localStorage.setItem('access_token', access_token);
            // Сохраняем новый токен и повторяем оригинальный запрос
            api.dispatch(setCredentials({token: access_token}));
            result = await baseQuery(args, api, extraOptions);
        } else {
            // Завершаем сессию при невозможности обновления токена
            api.dispatch(logout());
        }
    }

    return result;
};

// initialize an empty api service that we'll inject endpoints into later as needed
export const emptySplitApi = createApi({
    baseQuery: baseQueryWithReauth,
    endpoints: () => ({}),
    tagTypes: ["Chat"]
})