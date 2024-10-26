import Link from "next/link";

type Props = {};

export function Menu(props: Props) {
    return (
        <div className={"absolute top-0 left-0 h-full w-3/12 bg-gray-950 border-2 border-secondary rounded-2xl p-4"}>
            <ul className={"flex flex-col gap-2"}>
                <li className={"text-ellipsis overflow-hidden truncate bg-gray-800  p-1 cursor-pointer rounded-lg hover:bg-gray-700 border-2 border-transparent hover:border-primary "}>
                    <Link className={"font-medium"} href={"/"}>
                        Главная
                    </Link>
                </li>
                <li className={"text-ellipsis overflow-hidden truncate bg-gray-800  p-1 cursor-pointer rounded-lg hover:bg-gray-700 border-2 border-transparent hover:border-primary "}>
                    <Link className={"font-medium"} href={"/"}>
                        Главная
                    </Link>
                </li>
                <li className={"text-ellipsis overflow-hidden truncate bg-gray-800  p-1 cursor-pointer rounded-lg hover:bg-gray-700 border-2 border-transparent hover:border-primary "}>
                    <Link className={"font-medium"} href={"/"}>
                        Главная
                    </Link>
                </li>
                <li className={"text-ellipsis overflow-hidden truncate bg-gray-800  p-1 cursor-pointer rounded-lg hover:bg-gray-700 border-2 border-transparent hover:border-primary "}>
                    <Link className={"font-medium"} href={"/"}>
                        Главная
                    </Link>
                </li>
            </ul>
        </div>
    );
};