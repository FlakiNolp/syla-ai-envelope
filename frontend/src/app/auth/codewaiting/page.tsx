import { AuthForm } from "@/features/AuthForm"
import Link from "next/link";

const AuthPage = () => {
    return (

        <div className={"absolute w-full h-full flex flex-col gap-1.5 justify-center items-center"}>
            <h1 className={"text-4xl text-tertiary"}>Вам пришло письмо с кодом на почту!</h1>
            <Link className={"text-primary"} href={"/auth"}>Go back</Link>
        </div>

    )
}

export default AuthPage