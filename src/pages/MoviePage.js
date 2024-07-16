import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './MoviePage.css';

const MoviePage = () => {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const response = await fetch('http://localhost:5555/movies');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                // Add showDescription property to each movie
                const moviesWithDescription = data.map(movie => ({
                    ...movie,
                    showDescription: false
                }));
                setMovies(moviesWithDescription);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchMovies();
    }, []);

    const toggleDescription = (index) => {
        const updatedMovies = [...movies];
        updatedMovies[index].showDescription = !updatedMovies[index].showDescription;
        setMovies(updatedMovies);
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div className="movie-page-container">
            <h1>Movies</h1>
            <p>Here you can find all your favorite movies and write reviews! Dive into our extensive collection and share your thoughts with the community.</p>
            <ul className="movie-list">
                {movies.map((movie, index) => (
                    <li key={movie.id} className="movie-card">
                        {movie.poster_url && (
                            <img src={movie.poster_url} alt={movie.title} />
                        )}
                        <div className="movie-card-content">
                            <h2>{movie.title}</h2>
                            <p className={movie.showDescription ? 'show' : 'hide'}>{movie.description}</p>
                            <button className="btn-toggle-description" onClick={() => toggleDescription(index)}>
                                {movie.showDescription ? 'Hide Description' : 'Show Description'}
                            </button>
                            <Link to={`/review/${movie.id}`} className="btn-review">Write Review</Link>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MoviePage;
