import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import SignUp from "./components/SignUp";
import Login from "./components/Login";
import HomePage from "./pages/HomePage";
import MoviePage from "./pages/MoviePage";
import ProfilePage from "./pages/ProfilePage";
import ReviewPage from "./pages/ReviewPage";
import NavBar from "./components/NavBar";

const ProtectedRoute = ({ component: Component, ...rest }) => {
    const { currentUser } = useAuth();

    return currentUser ? <Component {...rest} /> : <Navigate to="/login" />;
};

const App = () => {
    return (
        <AuthProvider>
            <NavBar />
            <Routes>
                <Route path="/signup" element={<SignUp />} />
                <Route path="/login" element={<Login />} />
                <Route path="/home" element={<ProtectedRoute component={HomePage} />} />
                <Route path="/movie" element={<ProtectedRoute component={MoviePage} />} />
                <Route path="/profile" element={<ProtectedRoute component={ProfilePage} />} />
                <Route path="/review/:movieId" element={<ProtectedRoute component={ReviewPage} />} />
                <Route path="/" element={<ProtectedRoute component={HomePage} />} />
            </Routes>
        </AuthProvider>
    );
};

export default App;
