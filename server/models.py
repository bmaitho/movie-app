from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin': self.admin
        }

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    release_date = db.Column(db.String(50))
    director = db.Column(db.String(50))
    rating = db.Column(db.String(10))
    reviews = db.relationship('Review', backref='movie', lazy=True)
    poster_url = db.Column(db.String(255), nullable=True)

    def to_dict(self, rules=()):
        movie_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_date': self.release_date,
            'director': self.director,
            'rating': self.rating,
            'poster_url': self.poster_url
        }
        if '-reviews' not in rules:
            movie_dict['reviews'] = [review.to_dict() for review in self.reviews]
        return movie_dict

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    rating = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Define relationship to User
    user = db.relationship('User', backref='reviews', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    movies = db.relationship('MovieGenre', backref='genre', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class MovieGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'genre_id': self.genre_id
        }
