import React, { useState, useEffect } from 'react';
import './MoviePage.css';

function MoviePage() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('/movies')
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error('Error fetching movies:', error));
  }, []);

  return (
    <div className="movie-page">
      <h2>Movie List</h2>
      <ul>
        {movies.map(movie => (
          <li key={movie.id}>
            {movie.title} - {movie.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MoviePage;
