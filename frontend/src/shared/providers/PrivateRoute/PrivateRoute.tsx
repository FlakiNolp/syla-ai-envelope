'use client'
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function PrivateRoute({ children }) {
    const router = useRouter();
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        // Проверяем, что мы на клиенте, и доступен localStorage
        const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
        setIsAuthenticated(token);

        if (!token) {
            router.push('/auth');
        }
    }, [router]);

    // Пока состояние isAuthenticated не установлено, ничего не рендерим
    if (isAuthenticated === null) {
        return null; // Можно добавить компонент загрузки
    }

    return <>{children}</>;
}
