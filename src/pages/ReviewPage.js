import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const ReviewPage = () => {
    const { movieId } = useParams();
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await fetch(`http://localhost:5555/reviews/${movieId}`);
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
    }, [movieId]);

    const handleDelete = async (reviewId) => {
        try {
            const response = await fetch(`http://localhost:5555/reviews/${reviewId}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            setReviews(prevReviews => prevReviews.filter(review => review.id !== reviewId));
        } catch (error) {
            console.error('Error deleting review:', error);
        }
    };

    const handleUpdate = async (reviewId, updatedReview) => {
        try {
            const response = await fetch(`http://localhost:5555/reviews/${reviewId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedReview),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const updatedReviews = reviews.map(review =>
                review.id === reviewId ? { ...review, ...updatedReview } : review
            );
            setReviews(updatedReviews);
        } catch (error) {
            console.error('Error updating review:', error);
        }
    };

    const handleCreate = async (newReview) => {
        try {
            const response = await fetch('http://localhost:5555/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newReview),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const createdReview = await response.json();
            setReviews(prevReviews => [...prevReviews, createdReview]);
        } catch (error) {
            console.error('Error creating review:', error);
        }
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h1>Reviews for Movie {movieId}</h1>
            <ul>
                {reviews.map(review => (
                    <li key={review.id}>
                        <p>Rating: {review.rating}</p>
                        <p>{review.comment}</p>
                        <button onClick={() => handleDelete(review.id)}>Delete Review</button>
                        <button onClick={() => handleUpdate(review.id, { ...review, rating: 5 })}>Update Review</button>
                    </li>
                ))}
            </ul>
            <h2>Create New Review</h2>
            <ReviewForm onCreate={handleCreate} />
        </div>
    );
};

const ReviewForm = ({ onCreate }) => {
    const [rating, setRating] = useState(0);
    const [comment, setComment] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onCreate({ rating, comment });
        setRating(0);
        setComment('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Rating:
                <input type="number" value={rating} onChange={e => setRating(Number(e.target.value))} />
            </label>
            <label>
                Comment:
                <textarea value={comment} onChange={e => setComment(e.target.value)} />
            </label>
            <button type="submit">Submit Review</button>
        </form>
    );
};

export default ReviewPage;
