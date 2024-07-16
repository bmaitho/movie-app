import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ReviewPage.css';

const ReviewPage = () => {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();  // Import useNavigate from 'react-router-dom'

    useEffect(() => {
        const fetchMoviesWithReviews = async () => {
            try {
                const response = await fetch('http://localhost:5555/all_movies_with_reviews');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setMovies(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
    
        fetchMoviesWithReviews();
    }, []);
    

    const handleAddReviewClick = (movieId) => {
        navigate(`add-/review/${movieId}`);  // Ensure this matches the route defined in App.js
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="reviews-page-container">
            <h1>All Movies with Reviews</h1>
            {movies.map(movie => (
                <div key={movie.id} className="movie-section">
                    <h2>{movie.title}</h2>
                    <img src={movie.poster_url} alt={movie.title} className="movie-poster" />
                    <button className="add-review-button" onClick={() => handleAddReviewClick(movie.id)}>
                        Add Review
                    </button>
                    {movie.reviews.length > 0 ? (
                        <ul className="review-list">
                            {movie.reviews.map(review => (
                                <li key={review.id} className="review-card">
                                    <div className="review-card-content">
                                        <h3>{review.user ? review.user.username : 'Anonymous'}</h3>
                                        <p>{review.content}</p>
                                        <p>Rating: {review.rating}</p>
                                        <p>Posted on: {new Date(review.timestamp).toLocaleDateString()}</p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No reviews yet.</p>
                    )}
                </div>
            ))}
        </div>
    );
};

export default ReviewPage;
