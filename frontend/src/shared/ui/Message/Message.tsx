import classNames from "classnames"
import gsap from "gsap"
import TextPlugin from "gsap/TextPlugin"
import React, {useCallback, useState} from "react"
import Markdown from "react-markdown"
import {TypeAnimation} from "react-type-animation"
import type {IRole} from "@/entities/Chat"
import {Avatar} from "../Avatar/Avatar"
import cls from "./Message.module.scss"
import {useGSAP} from "@gsap/react"

gsap.registerPlugin(useGSAP, TextPlugin)

interface MessageProps {
    className?: string
    sender?: IRole
    content?: string
    isExample?: boolean
}

export const Message = (props: MessageProps) => {
    const [drawerIsOpen, setDrawerIsOpen] = useState(false)
    const openDrawer = useCallback(() => {
        setDrawerIsOpen(true)
    }, [])
    const closeDrawer = useCallback(() => {
        setDrawerIsOpen(false)
    }, [])
    const {
        className,
        sender,
        content,
        isExample = false
    } = props

    return (
        <div className={classNames(cls.Message, {}, [className, cls[sender || "user"]])}>
            <Avatar theme={sender}/>
            <div className={classNames(cls.content, {[cls.isExample]: isExample})}>
                {isExample ? <TypeAnimation cursor={false} sequence={[content as string]}/> :
                    <Markdown className={cls.markdown}>{content}</Markdown>}

            </div>
        </div>
    )
}
