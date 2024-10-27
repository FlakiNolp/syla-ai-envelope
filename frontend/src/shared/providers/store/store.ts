'use client'
import {configureStore, ReducersMapObject} from "@reduxjs/toolkit";
import {injectedRtkApi} from "@/shared/providers/store/Chat";
import apiReducer from './api/apiSlice';


export const rootReducer = {
    auth: apiReducer,
    [injectedRtkApi.reducerPath]: injectedRtkApi.reducer
}

export const store =  configureStore(
    {
        reducer: rootReducer,
        middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(injectedRtkApi.middleware),
    }
)
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch