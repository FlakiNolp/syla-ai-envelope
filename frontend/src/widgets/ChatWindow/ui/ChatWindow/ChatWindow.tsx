import classNames from "classnames";
import cls from "./ChatWindow.module.scss";
import {Message} from "@/shared/ui/Message/Message";
import {useEffect, useRef, useState} from "react";
import {useGSAP} from "@gsap/react";
import {gsap} from "gsap"
import OpenAI from "openai";
import {MessageSender} from "@/widgets/ChatWindow/ui/MessageSender/MessageSender";
import {MessageWidget} from "@/widgets/ChatWindow/ui/MessageWidget/MessageWidget";
import {useParams, usePathname, useRouter, useSearchParams} from "next/navigation";
import {usePostMessageMessagePostMutation} from "@/shared/providers/store/Chat";

type Props = {};
gsap.registerPlugin(useGSAP)

export function ChatWindow(props: Props) {
    const params = useSearchParams()
    const {id} = useParams()
    const router = useRouter()
    const [sendMessage, {
        isLoading
    }] = usePostMessageMessagePostMutation({fixedCacheKey: ("chat")})
    const [showAiAnswer, setShowAiAnswer] = useState(false)
    const tl = useRef(null)
    useGSAP(() => {
        tl.current = gsap.timeline()
            .from("." + cls.title, {
                opacity: 0,
                y: 100,
                duration: 1,
                ease: "power4.out"
            })
            .from("." + cls.description, {
                opacity: 0,
                y: 100,
                duration: 1,
                ease: "power4.out"
            })
    })
    useEffect(() => {
        setTimeout(() => setShowAiAnswer(true), 2000)

        async function checkName() {


        }
    }, [])
    return (

        <div className={classNames(cls.ChatWindow, {}, [])}>
            {
                (params.get("newChat") || id) ? (
                    <>
                        <MessageWidget messageIsLoading={isLoading}/>
                        <MessageSender sendMessage={sendMessage} isLoading={isLoading}/>
                    </>
                    ) :
                    (<div className={classNames(cls.MainWindow, {}, [])}>
                        <h1 className={cls.title}>Добро пожаловать в <span>Papper</span></h1>
                        <h2 className={cls.description}>Чат-бот по работе с документацией</h2>
                        <div className={cls.preview}>
                            <Message sender={"user"} content={"Привет, как тебя зовут?"} isExample/>
                            {showAiAnswer && <Message sender={"ai"} content={"Привет, меня зовут Papper"} isExample/>}
                        </div>
                    </div>)}
        </div>

    );
};