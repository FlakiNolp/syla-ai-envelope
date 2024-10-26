import type {Metadata} from "next";
import localFont from "next/font/local";
import "./globals.css";
import {Instrument_Sans} from "next/font/google";
import { AntdRegistry } from '@ant-design/nextjs-registry';

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
                className={`${saarFont.variable} ${instrumentSansFont.variable} bg-gray-800 text-white font-instrumentSans`}
            >
                <AntdRegistry>{children}</AntdRegistry>
            </body>
        </html>
    );
}
