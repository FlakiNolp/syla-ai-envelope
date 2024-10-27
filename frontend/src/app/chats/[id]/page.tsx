import {MainPage} from "@/views/MainPage";
import PrivateRoute from "@/shared/providers/PrivateRoute/PrivateRoute";

export default function Home() {

    return (
        <PrivateRoute>
            <MainPage/>
        </PrivateRoute>
    );
}
