'use client'
import { useRouter } from 'next/navigation';
import {useEffect, useState} from 'react';

export default function PrivateRoute({ children }) {
    const router = useRouter();
    const isAuthenticated = localStorage.getItem('access_token');

    useEffect(() => {

        if (!isAuthenticated) {
            router.push('/auth');
        }
    }, [isAuthenticated, router]);

    if (!isAuthenticated) {
        return null; // или загрузочный экран
    }

    return <>{children}</>;
}
