
import classNames from "classnames"

import cls from "./ChatsItem.module.scss"

interface ChatsItemProps {
    label: string
    id: string
}

export const ChatsItem = ({ label, id }: ChatsItemProps) => {

    return (
        <div className={classNames(cls.ChatsItem, {}, [])}>
            <div className={cls.label}>{label}</div>
        </div>
    )
}
