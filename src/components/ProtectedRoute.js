// src/components/ProtectedRoute.js
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "../firebaseConfig";

const ProtectedRoute = ({ component: Component, ...rest }) => {
    const [user, loading] = useAuthState(auth);

    if (loading) {
        return <div>Loading...</div>; // or a spinner
    }

    return user ? <Component {...rest} /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
