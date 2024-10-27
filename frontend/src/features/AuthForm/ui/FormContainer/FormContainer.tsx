import "./FormContainer.scss"
import {Form} from "antd"
import {memo, useState} from "react"
import axios from "axios"

import {Button} from "@/shared/ui/Button/Button"
import {FormInput} from "@/shared/ui/Input/Input"
import {useAppDispatch} from "@/shared/hooks/useAppDispatch";
import {setCredentials} from "@/shared/providers/store/api/apiSlice";
import {useRegistrationRegistrationGetQuery, useSignUpSignUpPostMutation} from "@/shared/providers/store/Chat";
import {useRouter} from "next/navigation";


export type FormType = "sign-up" | "sign-in";

interface FormContainerProps {
    className?: string,
    title: string,
    description?: string,
    buttonName: string,
    formType: FormType,
    handleToggle: () => void
}

export const FormContainer = (props: FormContainerProps) => {
    const [registerLogin, setRegisterLogin] = useState("")
    const [login, setLogin] = useState("")
    const [password, setPassword] = useState("")
    const [registerPassword, setRegisterPassword] = useState("")
    const dispatch = useAppDispatch()
    const router = useRouter()


    const {
        title,
        description,
        buttonName,
        formType,
        handleToggle
    } = props

    const isSignUp = formType === "sign-up"
    const onChangeLogin = (e: React.ChangeEvent<HTMLInputElement>) => {
        isSignUp ? setRegisterLogin(e.target.value) : setLogin(e.target.value)
    }
    const onChangePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        isSignUp ? setRegisterPassword(e.target.value) : setPassword(e.target.value)
    }
    const onLoginClick = async () => {
        try {
            if (isSignUp) {
                const response = await axios.post("http://31.129.50.189:8000/sign-up/", {
                    username: registerLogin,
                    password: registerPassword
                }, {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                })
                const status = response.status
                console.log(status)
                if (status === 202) {
                    router.push("/auth/codewaiting")
                }
            } else {
                const response = await axios.post("http://31.129.50.189:8001/token", {
                    username: login,
                    password: password
                }, {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    withCredentials: true
                })
                console.log(document.cookie)
                const {access_token, refresh_token} = response.data
                console.log(access_token)
                localStorage.setItem("access_token", access_token)
                localStorage.setItem("refresh_token", refresh_token)
                dispatch(setCredentials({token: access_token}))
                router.push("/")
            }
        } catch (e) {
            console.log(e)
        }

    }
    return (
        <>
            <div className={"form-container " + formType}>
                <Form
                    onFinish={onLoginClick}
                >
                    <h1>{title}</h1>
                    <span>{description}</span>

                    <Form.Item className="formItem" name="login"
                               rules={[{required: true, message: "Поле обязательно для заполнения"}]}
                    >
                        <FormInput value={isSignUp ? registerLogin : login} onChange={onChangeLogin} type="email"
                                   placeholder="Email"/>
                    </Form.Item>
                    <Form.Item className="formItem passwordItem" name="password"
                               rules={[{required: true, message: "Поле обязательно для заполнения"},
                                   {min: 3, message: "Минимальная длина 3 символа"},
                                   {max: 32, message: "Максимальная длина 32 символа"},
                                   {
                                       pattern: /(?=.*[a-z])/,
                                       message: "Пароль должен содержать хотя бы одну строчную букву"
                                   },
                                   {
                                       pattern: /(?=.*[A-Z])/,
                                       message: "Пароль должен содержать хотя бы одну заглавную букву"
                                   },
                                   {pattern: /(?=.*[0-9])/, message: "Пароль должен содержать хотя бы одну цифру"},
                                   {
                                       pattern: /(?=.*[!@#$%^&*().])/,
                                       message: "Пароль должен содержать хотя бы один специальный символ: !@#$%^&*()."
                                   }
                               ]}>
                        <FormInput value={isSignUp ? registerPassword : password} onChange={onChangePassword} isPassword
                                   placeholder="Пароль"/>
                    </Form.Item>
                    <Form.Item
                        htmlFor="submit"
                    >
                        <Button>{buttonName}</Button>
                    </Form.Item>
                </Form>
            </div>

        </>
    )
}
