// // middleware.js
// import { NextResponse } from 'next/server';
//
// export function middleware(request) {
//     const token = request.cookies.get('token'); // получаем токен из cookies
//
//     if (!token) {
//         return NextResponse.redirect(new URL('/auth', request.url));
//     }
//
//     return NextResponse.next();
// }
//
// export const config = {
//     matcher: ['/'], // указываем защищенные пути
// };
import { NextResponse } from 'next/server';

export const middleware = (req) => {
    if (req.nextUrl.pathname === '/') {
        const url = req.nextUrl.clone();  // Clone the URL to modify it
        url.pathname = '/chats';          // Set the new destination path
        return NextResponse.redirect(url); // Use the modified URL
    }
    return NextResponse.next();
};
