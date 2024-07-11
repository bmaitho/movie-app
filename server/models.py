from app import db
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('reviews', lazy=True))

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

class MovieGenre(db.Model):
    __tablename__ = 'movie_genre'
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), primary_key=True)

    movie = db.relationship('Movie', backref=db.backref('movie_genres', lazy=True))
    genre = db.relationship('Genre', backref=db.backref('movie_genres', lazy=True))
