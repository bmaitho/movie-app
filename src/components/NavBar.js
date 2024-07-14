// src/components/NavBar.js
import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import './NavBar.css';

const NavBar = () => {
    const { currentUser } = useAuth();

    if (!currentUser) return null;

    return (
        <nav>
            <ul>
                <li><Link to="/home">Home</Link></li>
                <li><Link to="/movie">Movies</Link></li>
                <li><Link to="/profile">Profile</Link></li>
                <li><Link to="/review">Reviews</Link></li>
            </ul>
        </nav>
    );
};

export default NavBar;
