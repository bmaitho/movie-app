import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './ReviewPage.css';

const ReviewPage = () => {
    const { movieId } = useParams();
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
                // Check if data is an array and if each review has the expected properties
                if (Array.isArray(data) && data.every(review => review.user && review.user.username)) {
                    setReviews(data);
                } else {
                    throw new Error('Unexpected data format');
                }
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchReviews();
    }, [movieId]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="review-page-container">
            <h1>Reviews</h1>
            <ul className="review-list">
                {reviews.map(review => (
                    <li key={review.id} className="review-card">
                        <div className="review-card-content">
                            {/* Check if review.user is defined */}
                            <h2>{review.user ? review.user.username : 'Anonymous'}</h2>
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
