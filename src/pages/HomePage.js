// src/pages/HomePage.js
import React from 'react';
import './HomePage.css';


const HomePage = () => {
    return (
        <div className="page-container home-page">
            <div className="page-overlay"></div>
            <div className="page-content">
                <h1 className="page-title">Welcome to Mtandao!</h1>
                <p className="app-description">Discover, Review, and Share Your Favorite Movies with MovieMania! Join our vibrant community of movie enthusiasts and dive into an endless collection of films, from timeless classics to the latest blockbusters. Rate and review movies, create your watchlist, and connect with fellow movie lovers. Your cinematic adventure starts here!</p>
            </div>
        </div>
    );
};

export default HomePage;
