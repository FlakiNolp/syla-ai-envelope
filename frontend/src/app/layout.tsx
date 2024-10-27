import type {Metadata} from "next";
import localFont from "next/font/local";
import "./globals.css";
import {Instrument_Sans} from "next/font/google";
import {AntdRegistry} from '@ant-design/nextjs-registry';
import {ConfigProvider} from "antd";
import {themeAnt} from "@/shared/config/theme";

import {StoreProvider} from "@/shared/providers/store/Provider";

export const metadata: Metadata = {
    title: "Envelope Chat",
    description: "Chat with Envelopes",
};

const instrumentSansFont = Instrument_Sans({
    subsets: ['latin'],
    weight: ['400', '500', '600', '700'],
    variable: '--font-instrument-sans',
});

const saarFont = localFont({
    src: './fonts/saar.otf',
    variable: '--font-saar',
})

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
        <body
            className={`${saarFont.variable} ${instrumentSansFont.variable}`}
        >
        <AntdRegistry>
            <ConfigProvider theme={themeAnt}>
                <StoreProvider>{children}</StoreProvider>
            </ConfigProvider>
        </AntdRegistry>
        </body>
        </html>
    );
}
