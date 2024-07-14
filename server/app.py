
# Standard library imports
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import requests

# Local imports
from config import app, db, api
from models import User, Movie, Review, Genre, MovieGenre

# Views go here!
class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_user = User(
                username=data['username'],
                email=data['email'],
                admin=False
            )
            new_user.password_hash = data['password']
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id

            return make_response(new_user.to_dict(), 201)
        except Exception as e:
            print(f"Exception: {e}")
            return make_response({'error': 'Invalid inputs'}, 400)

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized, please sign in'}, 401

        current_user = User.query.get(user_id)
        return current_user.to_dict(), 200

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            return make_response(user.to_dict(), 200)

        return {'error': 'Incorrect credentials'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class Home(Resource):
    def get(self):
        return '<h1> Movie Database API </h1>'

class Movies(Resource):
    def get(self):
        movies = [movie.to_dict(rules=('-reviews', )) for movie in Movie.query.all()]
        return make_response(movies, 200)
    
    def post(self):
        data = request.get_json()
        new_movie = Movie(
            title=data['title'],
            description=data['description'],
            release_date=data['release_date'],
            director=data['director'],
            rating=data['rating']
        )
        db.session.add(new_movie)
        db.session.commit()
        return make_response(new_movie.to_dict(), 201)

class MoviesByID(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        if movie is None:
            return make_response({'error': 'Movie not found'}, 404)
        return make_response(movie.to_dict(rules=('-reviews', )), 200)
    
    def patch(self, id):
        movie_to_update = Movie.query.get(id)
        if movie_to_update is None:
            return make_response({'error': 'Movie not found'}, 404)

        for key in request.json:
            setattr(movie_to_update, key, request.json[key])

        db.session.commit()
        return make_response(movie_to_update.to_dict(), 202)
    
    def delete(self, id):
        movie_to_delete = Movie.query.get(id)
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return make_response({'message': 'Movie deleted'}, 200)
        return {'error': 'Movie not found'}, 404

class Reviews(Resource):
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(reviews, 200)
    
    def post(self):
        data = request.get_json()
        new_review = Review(
            user_id=data['user_id'],
            movie_id=data['movie_id'],
            content=data['content'],
            rating=data['rating']
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(new_review.to_dict(), 201)

class Genres(Resource):
    def get(self):
        genres = [genre.to_dict() for genre in Genre.query.all()]
        return make_response(genres, 200)

class MovieGenres(Resource):
    def post(self):
        data = request.get_json()
        new_movie_genre = MovieGenre(
            movie_id=data['movie_id'],
            genre_id=data['genre_id']
        )
        db.session.add(new_movie_genre)
        db.session.commit()
        return make_response(new_movie_genre.to_dict(), 201)

# Route registrations
api.add_resource(Home, '/')
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Movies, '/movies')
api.add_resource(MoviesByID, '/movies/<int:id>')
api.add_resource(Reviews, '/reviews')
api.add_resource(Genres, '/genres')
api.add_resource(MovieGenres, '/movie_genres')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Movie Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))
    big_image = db.Column(db.String(200))
    genre = db.Column(db.String(50))
    thumbnail = db.Column(db.String(200))
    rating = db.Column(db.String(10))
    year = db.Column(db.Integer)
    imdbid = db.Column(db.String(20))
    imdb_link = db.Column(db.String(200))

@app.route('/')
def index():
    return make_response({'message': 'Welcome to the Movie Directory!'}, 200)

# Fetch movies from external API and populate database
@app.route('/fetch_movies', methods=['POST'])
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

# CRUD operations for movies
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.json
    new_movie = Movie(
        rank=data.get('rank'),
        title=data.get('title'),
        description=data.get('description'),
        image=data.get('image'),
        big_image=data.get('big_image'),
        genre=data.get('genre'),
        thumbnail=data.get('thumbnail'),
        rating=data.get('rating'),
        year=data.get('year'),
        imdbid=data.get('imdbid'),
        imdb_link=data.get('imdb_link')
    )
    db.session.add(new_movie)
    db.session.commit()
    return make_response({'message': 'Movie added successfully.'}, 201)

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if movie:
        movie_data = {
            'id': movie.id,
            'rank': movie.rank,
            'title': movie.title,
            'description': movie.description,
            'image': movie.image,
            'big_image': movie.big_image,
            'genre': movie.genre,
            'thumbnail': movie.thumbnail,
            'rating': movie.rating,
            'year': movie.year,
            'imdbid': movie.imdbid,
            'imdb_link': movie.imdb_link
        }
        return make_response(movie_data, 200)
    else:
        return make_response({'message': 'Movie not found.'}, 404)

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)
    if movie:
        data = request.json
        movie.rank = data.get('rank', movie.rank)
        movie.title = data.get('title', movie.title)
        movie.description = data.get('description', movie.description)
        movie.image = data.get('image', movie.image)
        movie.big_image = data.get('big_image', movie.big_image)
        movie.genre = data.get('genre', movie.genre)
        movie.thumbnail = data.get('thumbnail', movie.thumbnail)
        movie.rating = data.get('rating', movie.rating)
        movie.year = data.get('year', movie.year)
        movie.imdbid = data.get('imdbid', movie.imdbid)
        movie.imdb_link = data.get('imdb_link', movie.imdb_link)
        
        db.session.commit()
        return make_response({'message': 'Movie updated successfully.'}, 200)
    else:
        return make_response({'message': 'Movie not found.'}, 404)

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return make_response({'message': 'Movie deleted successfully.'}, 200)
    else:
        return make_response({'message': 'Movie not found.'}, 404)

@app.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    movies_list = [{
        'id': movie.id,
        'rank': movie.rank,
        'title': movie.title,
        'description': movie.description,
        'image': movie.image,
        'big_image': movie.big_image,
        'genre': movie.genre,
        'thumbnail': movie.thumbnail,
        'rating': movie.rating,
        'year': movie.year,
        'imdbid': movie.imdbid,
        'imdb_link': movie.imdb_link
    } for movie in movies]
    return make_response({'movies': movies_list}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
