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

const ProtectedRoute = ({ children }) => {
    const { currentUser } = useAuth();
    return currentUser ? children : <Navigate to="/login" />;
};

const App = () => {
    return (
        <AuthProvider>
            <NavBar />
            <Routes>
                <Route path="/signup" element={<SignUp />} />
                <Route path="/login" element={<Login />} />
                <Route path="/home" element={
                    <ProtectedRoute>
                        <HomePage />
                    </ProtectedRoute>
                } />
                <Route path="/movie" element={
                    <ProtectedRoute>
                        <MoviePage />
                    </ProtectedRoute>
                } />
                <Route path="/profile" element={
                    <ProtectedRoute>
                        <ProfilePage />
                    </ProtectedRoute>
                } />
                <Route path="/review/:movieId" element={
                    <ProtectedRoute>
                        <ReviewPage />
                    </ProtectedRoute>
                } />
                <Route path="/add-review/:movieId" element={
                    <ProtectedRoute>
                        <ReviewPage />  {/* This is a placeholder for adding a review */}
                    </ProtectedRoute>
                } />
                <Route path="/" element={
                    <ProtectedRoute>
                        <HomePage />
                    </ProtectedRoute>
                } />
            </Routes>
        </AuthProvider>
    );
};

export default App;
