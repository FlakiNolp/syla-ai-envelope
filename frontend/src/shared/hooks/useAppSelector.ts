'use client';
import {useSelector} from "react-redux";
import {RootState} from "@/shared/providers/store/store";

export const useAppSelector = useSelector.withTypes<RootState>()