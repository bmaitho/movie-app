import React, { useState, useEffect } from 'react';
import './MoviePage.css';

function MoviePage() {
  const [movies, setMovies] = useState([]);
  const fullText = "Here you can find all your favorite movies and write reviews! Dive into our extensive collection and share your thoughts with the community.";

  useEffect(() => {
    fetch('/movies')
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error('Error fetching movies:', error));
  }, []);

  return (
    <div className="movie-page page-container">
      <div className="page-overlay"></div>
      <div className="page-content">
        <h1 className="page-title">Movies</h1>
        <p className="app-description">{fullText}</p>
        <ul>
          {movies.map(movie => (
            <li key={movie.id}>
              {movie.title} - {movie.description}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default MoviePage;
