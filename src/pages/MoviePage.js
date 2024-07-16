import React, { useState, useEffect } from 'react';
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
                console.log(data);
                setMovies(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchMovies();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h1>Movies</h1>
            <p>Here you can find all your favorite movies and write reviews! Dive into our extensive collection and share your thoughts with the community.</p>
            <ul>
                {movies.map(movie => (
                    <li key={movie.id}>
                        {movie.poster_url && (
                            <img src={movie.poster_url} alt={movie.title} style={{ width: '150px', height: 'auto' }} />

                        )}
                        <h2>{movie.title}</h2>
                        <p>{movie.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default MoviePage;
