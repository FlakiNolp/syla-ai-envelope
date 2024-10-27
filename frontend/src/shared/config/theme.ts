'use client';

import {theme} from "antd";

export const themeAnt = {
    algorithm: theme.darkAlgorithm,
    token: {
        colorPrimary: "#03FE33",
        fontFamily: "Panagram, sans-serif"
    },
    components: {
        Statistic: {
            contentFontSize: 20,
            titleFontSize: 20
        },
        Timeline: {
            dotBg: "transparent"
        }
    }
}