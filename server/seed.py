#!/usr/bin/env python3

from app import app
from models import db, User, Movie, Review, Genre

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables and create new ones
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
            Movie(
                title="Inception",
                description="A thief who steals corporate secrets through the use of dream-sharing technology.",
                release_date="2010-07-16",
                director="Christopher Nolan",
                rating="8.8",
                poster_url="https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p7825626_p_v8_ae.jpg"
            ),
            Movie(
                title="The Matrix",
                description="A computer hacker learns from mysterious rebels about the true nature of his reality.",
                release_date="1999-03-31",
                director="The Wachowskis",
                rating="8.7",
                poster_url="https://images.bauerhosting.com/legacy/empire-tmdb/films/603/images/7u3pxc0K1wx32IleAkLv78MKgrw.jpg?ar=16:9&fit=crop&crop=top"
            ),
            Movie(
                title="Interstellar",
                description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                release_date="2014-11-07",
                director="Christopher Nolan",
                rating="8.6",
                poster_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSVVazaukDPzzzl1gMZ4_0EVjGXVMlqk5VpaA&s"
            ),
            Movie(
                title="Pulp Fiction",
                description="The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                release_date="1994-10-14",
                director="Quentin Tarantino",
                rating="8.9",
                poster_url="https://cdn.britannica.com/66/141066-050-36AB089D/John-Travolta-Samuel-L-Jackson-Pulp-Fiction.jpg"
            ),
            Movie(
                title="The Dark Knight",
                description="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
                release_date="2008-07-18",
                director="Christopher Nolan",
                rating="9.0",
                poster_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3ekE6Hhz9gvIbiFSUPxt-FyAh4zXTXX0bjQ&s"
            ),
            Movie(
                title="The Godfather",
                description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                release_date="1972-03-24",
                director="Francis Ford Coppola",
                rating="9.2",
                poster_url="https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"
            ),
            Movie(
                title="Forrest Gump",
                description="The presidencies of Kennedy and Johnson, the Vietnam War, the civil rights movement, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
                release_date="1994-07-06",
                director="Robert Zemeckis",
                rating="8.8",
                poster_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvxY-v3jqcL0Z01G-KuVR_3h1sxRPUctyrKg&s"
            ),
            Movie(
                title="Fight Club",
                description="An insomniac office worker and a soap salesman build a global organization to help vent male aggression.",
                release_date="1999-10-15",
                director="David Fincher",
                rating="8.8",
                poster_url="https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"
            ),
            Movie(
                title="The Shawshank Redemption",
                description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                release_date="1994-09-23",
                director="Frank Darabont",
                rating="9.3",
                poster_url="https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg"
            ),
            Movie(
                title="Gladiator",
                description="A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
                release_date="2000-05-05",
                director="Ridley Scott",
                rating="8.5",
                poster_url="https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
            ),
            Movie(
                title="Joker",
                description="In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral that leads him to become the infamous Joker.",
                release_date="2019-10-04",
                director="Todd Phillips",
                rating="8.4",
                poster_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQP7TzsGto_FJI2I9IibPV1GWd--ki-_NAAYQ&s"
            ),
        ]
        for movie in movies:
            db.session.add(movie)
        db.session.commit()

        print("Seeding users...")
        users = [
            User(username='john_doe', email='john@example.com', password_hash='password123', admin=False),
            User(username='admin_user', email='admin@example.com', password_hash='adminpassword', admin=True),
        ]
        for user in users:
            db.session.add(user)
        db.session.commit()

        print("Seeding reviews...")
        reviews = [
            Review(user_id=1, movie_id=1, content="Amazing movie!", rating="9.0"),
            Review(user_id=2, movie_id=2, content="A true classic.", rating="8.5"),
            Review(user_id=1, movie_id=3, content="A mind-bending journey through space.", rating="8.8"),
            Review(user_id=2, movie_id=4, content="Tarantino's best work!", rating="9.2"),
            Review(user_id=1, movie_id=5, content="The best Batman movie ever.", rating="9.5"),
            Review(user_id=2, movie_id=6, content="A masterpiece of crime cinema.", rating="9.3"),
            Review(user_id=1, movie_id=7, content="A heartwarming and profound story.", rating="8.7"),
            Review(user_id=2, movie_id=8, content="A dark and gritty look at modern masculinity.", rating="8.9"),
            Review(user_id=1, movie_id=9, content="An intense and moving film.", rating="9.0"),
            Review(user_id=2, movie_id=10, content="A powerful and disturbing character study.", rating="8.4"),
        ]
        for review in reviews:
            db.session.add(review)
        db.session.commit()

        print("Seeding complete.")
