from flask import Blueprint, request, jsonify, make_response
import requests
from config import db
from models import Movie

fetch_movies_bp = Blueprint('fetch_movies_bp', __name__)

@fetch_movies_bp.route('/fetch_movies', methods=['POST'])
def fetch_movies():
    url = "https://imdb-top-100-movies.p.rapidapi.com/top32"
    headers = {
        "x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com",
        "x-rapidapi-key": "24e2f822dfmshf8b3b3ed65b271fp1d7e64jsna998c37aac2e"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        movies = response.json()
        for movie_data in movies:
            movie = Movie(
                rank=movie_data.get('rank'),
                title=movie_data.get('title'),
                description=movie_data.get('description'),
                image=movie_data.get('image'),
                big_image=movie_data.get('big_image'),
                genre=movie_data.get('genre'),
                thumbnail=movie_data.get('thumbnail'),
                rating=movie_data.get('rating'),
                year=movie_data.get('year'),
                imdbid=movie_data.get('imdbid'),
                imdb_link=movie_data.get('imdb_link')
            )
            db.session.add(movie)
        db.session.commit()
        return make_response({'message': 'Movies fetched and added to the database.'}, 201)
    else:
        return make_response({'message': 'Failed to fetch movies.'}, 400)
