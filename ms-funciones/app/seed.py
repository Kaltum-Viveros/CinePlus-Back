from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models import Funcion


MOVIES = [
    {
        "movie_id": 1,
        "movie_title": "Inception",
        "room": "Sala 1"
    },
    {
        "movie_id": 2,
        "movie_title": "The Dark Knight",
        "room": "Sala 2"
    },
    {
        "movie_id": 3,
        "movie_title": "Interstellar",
        "room": "Sala 3"
    },
    {
        "movie_id": 4,
        "movie_title": "Spider-Man: No Way Home",
        "room": "Sala 4"
    },
    {
        "movie_id": 5,
        "movie_title": "Coco",
        "room": "Sala 5"
    },
    {
        "movie_id": 6,
        "movie_title": "The Conjuring",
        "room": "Sala 6"
    },
    {
        "movie_id": 7,
        "movie_title": "Toy Story 4",
        "room": "Sala 7"
    },
    {
        "movie_id": 8,
        "movie_title": "Dune",
        "room": "Sala 8"
    },
    {
        "movie_id": 9,
        "movie_title": "Avengers: Endgame",
        "room": "Sala 9"
    },
    {
        "movie_id": 10,
        "movie_title": "The Notebook",
        "room": "Sala 10"
    },
]

TIMES = ["10:00", "12:30", "15:00", "17:30", "20:00", "22:30"]


def seed_funciones(db: Session):
    total = db.query(Funcion).count()

    if total > 0:
        return

    today = date.today()

    for day_offset in range(14):
        current_date = today + timedelta(days=day_offset)

        for movie in MOVIES:
            for time in TIMES:
                funcion = Funcion(
                    movie_id=movie["movie_id"],
                    movie_title=movie["movie_title"],
                    date=current_date,
                    time=time,
                    room=movie["room"],
                    available=True
                )
                db.add(funcion)

    db.commit()