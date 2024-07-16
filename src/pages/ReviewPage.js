import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './ReviewPage.css'; // Create a ReviewPage.css file for styling

const ReviewPage = () => {
    const { movieId } = useParams(); // Extract movieId from URL params
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await fetch(`http://localhost:5555/movies/${movieId}/reviews`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setReviews(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchReviews();
    }, [movieId]); // Fetch reviews whenever movieId changes

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="review-page-container">
            <h1>Reviews</h1>
            <ul className="review-list">
                {reviews.map(review => (
                    <li key={review.id} className="review-card">
                        <div className="review-card-content">
                            <h2>{review.user.username}</h2>
                            <p>{review.content}</p>
                            <p>Rating: {review.rating}</p>
                            <p>Posted on: {new Date(review.timestamp).toLocaleDateString()}</p>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ReviewPage;
