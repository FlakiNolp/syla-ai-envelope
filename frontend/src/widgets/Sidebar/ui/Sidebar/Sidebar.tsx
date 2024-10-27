import {Menu, MenuProps} from "antd"
import classNames from "classnames"
import cls from "./Sidebar.module.scss"
import {useMemo} from "react";
import {ChatsItem} from "../ChatsItem/ChatsItem";
import {useRouter} from "next/navigation";
import {PlusCircleOutlined} from "@ant-design/icons"
import {useGetChatsChatsGetQuery} from "@/shared/providers/store/Chat";

type MenuItem = Required<MenuProps>["items"][number]

interface SidebarProps {
    width?: number
    isMenuOpen?: boolean
    setIsMenuOpen?: React.Dispatch<React.SetStateAction<boolean>>
}



export const Sidebar = ({width, isMenuOpen, setIsMenuOpen}: SidebarProps) => {
    const {data, error, isLoading} = useGetChatsChatsGetQuery({})
    const router = useRouter()
    console.log(data)
    const chatsItems = useMemo(
        () => data?.chats?.map((item) => ({
            key: item.chat_id,
            label: <ChatsItem label={item.chat_name} id={String(item.chat_id)}/>,
            onClick: () => router.push(`/chats/${item.chat_id}`),
        })), [router, data?.chats])

    const handleNewChat = () => {
        router.push('/?newChat=true')
    }
    const items: MenuItem[] = [
        {
            key: "2",
            icon: <PlusCircleOutlined style={{fontSize: "20px", marginTop: "4px"}}/>,
            label: "Создать новый чат",
            onClick: handleNewChat
        },
        {
            key: "0",
            label: "Чаты",
            children: chatsItems
        },
    ]

    const menuMods = {
        [cls.menuOpen]: isMenuOpen
    }
    return (
        <>
            <Menu
                className={classNames(cls.Menu, menuMods)}
                style={{width: '300px'}}
                items={items}
                mode="inline"
                openKeys={["0"]}
            />
        </>

    )
}
