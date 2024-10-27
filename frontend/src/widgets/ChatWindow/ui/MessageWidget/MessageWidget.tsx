import {Skeleton} from "antd"
import classNames from "classnames"

import {memo, useEffect, useMemo, useRef} from "react"

import {Message} from "@/shared/ui/Message/Message"
import cls from "./MessageWidget.module.scss"
import {IRole} from "@/entities/Chat";
import {useGetMessageMessageGetQuery, usePostMessageMessagePostMutation} from "@/shared/providers/store/Chat";
import {useParams, useSearchParams} from "next/navigation";

interface MessageWidgetProps {
    className?: string;
    messageIsLoading?: boolean
}

export const MessageWidget = ({className, messageIsLoading}: MessageWidgetProps) => {
    const params = useSearchParams()
    const chatRef = useRef(null)
    const isNewChat = params.get("newChat") === "true"
    const {id} =  useParams()

    let data, error, isLoadingHistory;

    if (id) {
        const {data: queryData, error: queryError, isLoading: queryIsLoading} = useGetMessageMessageGetQuery({
            chatId: id as string
        });

        data = queryData;
        error = queryError;
        isLoadingHistory = queryIsLoading;
    }


    const currentChat: { text: string, author: IRole, pics: string[] }[] = data?.messages.map((item) => {
        return { text: item.text, author: item.author, pics: item.pics }
    })
    const messages = useMemo(() => currentChat?.map((item) => {
        return {content: item.text, sender: item.author, pics: item.pics}
    }), [currentChat])
    useEffect(() => {
        chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: "smooth" })
    }, [currentChat])
    return (
        <>
            <div ref={chatRef} className={classNames(cls.MessageWidget, {}, [className])}>
                {isLoadingHistory
                    ? <Skeleton active/>
                    : (messages?.length && messages?.length > 0)
                        ? (<>

                            {messages?.map((item) => <Message className={"message"} key={Math.random()}
                                                              sender={item.sender} pics={item.pics} content={item.content}/>)}
                            {messageIsLoading && <Skeleton avatar paragraph={{ rows: 3 }} active />}
                        </>)
                        : (
                            <div className={classNames(cls.EmptyChat, {}, [className])}>
                                <div className={cls.text}>С чего бы начать?</div>
                                <div className={cls.description}>Задайте любой вопрос и наш ИИ ответит на него...</div>
                            </div>
                        )}
            </div>
        </>
    )
}
