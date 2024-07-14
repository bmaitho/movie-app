import React, { useState, useEffect } from 'react';
import './ReviewPage.css';

function ReviewPage() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch('/reviews')
      .then(response => response.json())
      .then(data => setReviews(data))
      .catch(error => console.error('Error fetching reviews:', error));
  }, []);

  return (
    <div className="review-page">
      <h2>Review List</h2>
      <ul>
        {reviews.map(review => (
          <li key={review.id}>
            {review.content} - {review.rating}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReviewPage;
