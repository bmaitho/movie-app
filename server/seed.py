#!/usr/bin/env python3

from faker import Faker
from app import app
from models import db, User, Movie, Review, Genre, MovieGenre

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("Seeding genres...")
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Thriller']
        for genre_name in genres:
            genre = Genre(name=genre_name)
            db.session.add(genre)

        db.session.commit()

        print("Seeding movies...")
        movies = [
            Movie(title="Inception", description="A thief who steals corporate secrets through the use of dream-sharing technology.", release_date="2010-07-16", director="Christopher Nolan", rating=8.8),
            Movie(title="The Matrix", description="A computer hacker learns from mysterious rebels about the true nature of his reality.", release_date="1999-03-31", director="The Wachowskis", rating=8.7),
        ]
        for movie in movies:
            db.session.add(movie)

        db.session.commit()

        print("Seeding users...")
        users = [
            User(username='john_doe', email='john@example.com', wallet=100.0, admin=False),
            User(username='admin_user', email='admin@example.com', wallet=500.0, admin=True),
        ]
        for user in users:
            db.session.add(user)

        db.session.commit()

        print("Seeding reviews...")
        reviews = [
            Review(user_id=1, movie_id=1, content="Amazing movie!", rating=9.0),
            Review(user_id=2, movie_id=2, content="A true classic.", rating=8.5),
        ]
        for review in reviews:
            db.session.add(review)

        db.session.commit()

        print("Seeding complete.")
