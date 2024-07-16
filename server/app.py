from flask_restful import Resource
from flask import Flask, request, session, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import requests

# Local imports
from config import app, db, api
from models import User, Movie, Review, Genre, MovieGenre
from fetch_movies import fetch_movies_bp

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
        movies = Movie.query.all()
        for movie in movies:
            print(movie.poster_url)  # Debugging: print URLs to ensure they are correct
        movies_dict = [movie.to_dict(rules=('-reviews', )) for movie in movies]
        return make_response(movies_dict, 200)

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

class ReviewsByMovie(Resource):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            return make_response({'error': 'Movie not found'}, 404)

        reviews = Review.query.filter_by(movie_id=movie_id).all()
        reviews_dict = [
            {
                "id": review.id,
                "content": review.content,
                "rating": review.rating,
                "timestamp": review.timestamp.isoformat(),
                "movie": {
                    "id": movie.id,
                    "title": movie.title,
                    "poster_url": movie.poster_url
                }
            }
            for review in reviews
        ]
        return make_response(reviews_dict, 200)

class AllMoviesWithReviews(Resource):
    def get(self):
        movies = Movie.query.all()
        movies_dict = [movie.to_dict(rules=()) for movie in movies]
        
        # Get reviews for each movie
        for movie in movies_dict:
            movie_id = movie['id']
            reviews = Review.query.filter_by(movie_id=movie_id).all()
            movie['reviews'] = [review.to_dict() for review in reviews]
        
        return make_response(movies_dict, 200)


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
api.add_resource(ReviewsByMovie, '/movies/<int:movie_id>/reviews')
api.add_resource(Genres, '/genres')
api.add_resource(MovieGenres, '/movie_genres')
api.add_resource(AllMoviesWithReviews, '/all_movies_with_reviews')

# Register blueprint
app.register_blueprint(fetch_movies_bp)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
