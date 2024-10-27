import {SendOutlined} from "@ant-design/icons"
import {Button} from "antd"
import classNames from "classnames"
import {memo, useCallback, useState} from "react"
import {TextField} from "@/shared/ui/TextField/TextField"
import cls from "./MessageSender.module.scss"
import {useParams, useRouter, useSearchParams} from "next/navigation";
import OpenAI from "openai";
import {
    CreateChatCreateChatPutApiArg, JsonMessage, PostMessageMessagePostApiArg,
    useCreateChatCreateChatPutMutation, usePostMessageMessagePostMutation
} from "@/shared/providers/store/Chat";
import {FetchBaseQueryError, FetchBaseQueryMeta, MutationDefinition, QueryReturnValue} from "@reduxjs/toolkit/query";
// @ts-ignore
import {MutationTrigger} from "@reduxjs/toolkit/src/query/react/buildHooks";

interface MessageSenderProps {
    className?: string
    sendMessage?: MutationTrigger<MutationDefinition<Omit<PostMessageMessagePostApiArg, "authorization">, (args: any, api: any, extraOptions: any) => Promise<QueryReturnValue<unknown, FetchBaseQueryError, FetchBaseQueryMeta>>, "Chat", JsonMessage, "api">>
    isLoading?: boolean
}

export const MessageSender = memo(({className, sendMessage, isLoading}: MessageSenderProps) => {
    const [createChat, {error, data: chat}] = useCreateChatCreateChatPutMutation({})
    const {id} = useParams()
    const router = useRouter()
    const searchParams = useSearchParams()
    const [message, setMessage] = useState("")
    const sendMessageHandle = useCallback(async () => {
        async function getChatName() {
            const openai = new OpenAI({
                baseURL: "https://fpuuggyfqm4rkc-8000.proxy.runpod.net/v1",
                apiKey: "1",
                dangerouslyAllowBrowser: true
            });
            const completion = await openai.chat.completions.create({
                model: "Qwen/Qwen2-VL-7B-Instruct",
                messages: [
                    {
                        role: "system",
                        content: "Ты определить названия беседы по первому сообщению. Твоя задача определить название беседы. Ты должен определять кратко ёмко и чётко"
                    },
                    {
                        role: "user",
                        content: message,
                    },
                ],
                max_tokens: 25,
                temperature: 0.3
            });
            return completion.choices[0].message.content
        }


        const isNewChat = searchParams.get("newChat")
        if (isNewChat) {
            const newChatName = await getChatName()
            const result = await createChat({
                createChatRequestSchema: {"chat-name": newChatName}
            });
            router.push(`/chats/${result.data.chat_id}`)
            console.log(result.data)
            await sendMessage({
                receivedMessageRequestSchema: {
                    message,
                    "chat_id": String(result.data.chat_id)
                }
            },)


        } else {
            await sendMessage({
                receivedMessageRequestSchema: {
                    message,
                    "chat_id": String(id)
                }
            })
        }
        setMessage("")
    }, [searchParams, message, createChat, router, sendMessage, id])
    const handleChangeTextField = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(e.target.value)
    }, [setMessage])
    return (
        <div className={classNames(cls.MessageSender, {}, [className])}>
            <TextField disabled={isLoading} onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    sendMessageHandle()
                }
            }} value={message} onChange={handleChangeTextField} className={cls.textField}/>
            <Button loading={isLoading} size="large" disabled={isLoading || message.length === 0} className={cls.button}
                    type="text" onClick={sendMessageHandle}
                    icon={<SendOutlined style={{color: "var(--primary-color)", fontSize: "var(--font-size-l)"}}/>}/>
        </div>
    )
})
