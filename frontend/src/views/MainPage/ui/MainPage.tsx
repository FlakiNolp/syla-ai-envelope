'use client';

import classNames from "classnames"
import { useEffect, useState } from "react"
import cls from "./MainPage.module.scss"
import {Sidebar} from "@/widgets/Sidebar";
import {ChatWindow} from "@/widgets/ChatWindow";

export const MainPage = () => {
    const [width, setWidth] = useState(0)
    const [isMenuOpen, setIsMenuOpen] = useState(false)
    useEffect(() => {
        // Function to update the width
        const handleResize = () => {
            setWidth(window.innerWidth);
        };

        // Set the initial width
        handleResize();

        // Add event listener for resize
        window.addEventListener('resize', handleResize);

        // Cleanup event listener on component unmount
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
    return (
        <div className={classNames(cls.LayoutPage)}>
            {/*<Header isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />*/}
            <div className={cls.Layout}>
                <Sidebar setIsMenuOpen={setIsMenuOpen} isMenuOpen={isMenuOpen} width={width} />
                <ChatWindow/>
            </div>
        </div>
    )
}

