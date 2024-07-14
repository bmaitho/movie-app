// src/pages/ProfilePage.js
import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const ProfilePage = () => {
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/login');
        } catch (error) {
            console.error('Failed to logout:', error);
        }
    };

    return (
        <div>
            <h1>Profile Page</h1>
            <p>Welcome, {currentUser && currentUser.email}</p>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default ProfilePage;
