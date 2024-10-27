import {emptySplitApi as api} from "./test";
import {IRole} from "@/entities/Chat";

export const injectedRtkApi = api.injectEndpoints({
    endpoints: (build) => ({
        signUpSignUpPost: build.mutation<
            SignUpSignUpPostApiResponse,
            SignUpSignUpPostApiArg
        >({
            query: (queryArg) => ({
                url: `/sign-up`,
                method: "POST",
                body: queryArg.bodySignUpSignUpPost,
            }),
        }),
        registrationRegistrationGet: build.query<
            RegistrationRegistrationGetApiResponse,
            RegistrationRegistrationGetApiArg
        >({
            query: (queryArg) => ({
                url: `/registration`,
                params: {
                    token: queryArg.token,
                },
            }),
        }),
        createChatCreateChatPut: build.mutation<
            CreateChatCreateChatPutApiResponse,
            Omit<CreateChatCreateChatPutApiArg, "authorization"> // Убираем authorization из аргументов
        >({
            query: (queryArg) => ({
                url: `/create-chat`,
                method: "PUT",
                body: queryArg.createChatRequestSchema,
            }),
            invalidatesTags: ["Chat"],
        }),
        getChatsChatsGet: build.query<
            GetChatsChatsGetApiResponse,
            Omit<GetChatsChatsGetApiArg, "authorization"> // Убираем authorization из аргументов
        >({
            query: () => ({
                url: `/chats`,
            }),
            providesTags: ["Chat"],
        }),
        postMessageMessagePost: build.mutation<
            PostMessageMessagePostApiResponse,
            Omit<PostMessageMessagePostApiArg, "authorization"> // Убираем authorization из аргументов
        >({
            query: (queryArg) => ({
                url: `/message`,
                method: "POST",
                body: queryArg.receivedMessageRequestSchema,
            }),
            async onQueryStarted(message, {dispatch, queryFulfilled}) {
                console.log(message.receivedMessageRequestSchema.message);
                dispatch(injectedRtkApi.util.updateQueryData("getMessageMessageGet", {
                    chatId:
                    message.receivedMessageRequestSchema.chat_id
                }, (draft) => {
                draft.messages.push({
                    id: String(Math.random()),
                    chat_id: message.receivedMessageRequestSchema.chat_id,
                    text: message.receivedMessageRequestSchema.message,
                    author: "user"
                })
                }))
                queryFulfilled.then((answer) => {
                    dispatch(injectedRtkApi.util.updateQueryData("getMessageMessageGet", {
                        chatId:
                        message.receivedMessageRequestSchema.chat_id
                    }, (draft) => {
                        draft.messages.push({
                            id: answer.data.id,
                            chat_id: answer.data.chat_id,
                            text: answer.data.text,
                            author: answer.data.author
                        })
                    }))
                })
            },
        }),
        getMessageMessageGet: build.query<
            GetMessageMessageGetApiResponse,
            Omit<GetMessageMessageGetApiArg, "authorization"> // Убираем authorization из аргументов
        >({
            query: (queryArg) => ({
                url: `/message`,
                params: {
                    chat_id: queryArg.chatId,
                },
            }),
        }),
    }),
    overrideExisting: false,
});

export {injectedRtkApi as chatApi};
export type SignUpSignUpPostApiResponse = any;
export type SignUpSignUpPostApiArg = {
    bodySignUpSignUpPost: BodySignUpSignUpPost;
};
export type RegistrationRegistrationGetApiResponse = any;
export type RegistrationRegistrationGetApiArg = {
    token: string;
};
export type CreateChatCreateChatPutApiResponse = CreateChatResponseSchema;
export type CreateChatCreateChatPutApiArg = {
    createChatRequestSchema: CreateChatRequestSchema;
};
export type GetChatsChatsGetApiResponse = GetChatsResponseSchema;
export type GetChatsChatsGetApiArg = Record<string, never>;
export type PostMessageMessagePostApiResponse = JsonMessage;
export type PostMessageMessagePostApiArg = {
    receivedMessageRequestSchema: ReceivedMessageRequestSchema;
};
export type GetMessageMessageGetApiResponse = GetHistoryResponseSchema;
export type GetMessageMessageGetApiArg = {
    chatId: string;
};

export type ErrorSchema = {
    error: string;
};
export type ValidationError = {
    loc: (string | number)[];
    msg: string;
    type: string;
};
export type HttpValidationError = {
    detail?: ValidationError[];
};
export type BodySignUpSignUpPost = {
    grant_type?: string | null;
    username: string;
    password: string;
    scope?: string;
    client_id?: string | null;
    client_secret?: string | null;
};
export type CreateChatResponseSchema = {
    chat_id: string;
};
export type CreateChatRequestSchema = {
    "chat-name": string;
};
export type JsonChat = {
    chat_id: string;
    chat_name: string;
};
export type GetChatsResponseSchema = {
    chats: JsonChat[];
};
export type JsonMessage = {
    id: string;
    chat_id: string;
    author: IRole;
    text: string;
    documents?: string[] | null;
};
export type ReceivedMessageRequestSchema = {
    message: string;
    chat_id: string;
};
export type GetHistoryResponseSchema = {
    messages: JsonMessage[];
};

export const {
    useSignUpSignUpPostMutation,
    useRegistrationRegistrationGetQuery,
    useCreateChatCreateChatPutMutation,
    useGetChatsChatsGetQuery,
    usePostMessageMessagePostMutation,
    useGetMessageMessageGetQuery,
} = injectedRtkApi;
