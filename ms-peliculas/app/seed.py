from sqlalchemy.orm import Session
from app.models import Pelicula


PELICULAS_INICIALES = [
    {
        "title": "Avatar: El Camino del Agua",
        "genre": "Ciencia ficción",
        "duration": "192 min",
        "poster": "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
        "synopsis": "Jake Sully vive con su nueva familia formada en Pandora, pero una antigua amenaza regresa.",
        "trailerUrl": "https://www.youtube.com/watch?v=d9MyW72ELq0",
        "price": 85.0
    },
    {
        "title": "Spider-Man: No Way Home",
        "genre": "Acción",
        "duration": "148 min",
        "poster": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
        "synopsis": "Peter Parker enfrenta las consecuencias de revelar su identidad como Spider-Man.",
        "trailerUrl": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
        "price": 80.0
    },
    {
        "title": "Intensamente 2",
        "genre": "Animación",
        "duration": "96 min",
        "poster": "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg",
        "synopsis": "Riley entra en la adolescencia y nuevas emociones aparecen en su mente.",
        "trailerUrl": "https://www.youtube.com/watch?v=LEjhY15eCx0",
        "price": 75.0
    },
    {
        "title": "Dune: Parte Dos",
        "genre": "Ciencia ficción",
        "duration": "166 min",
        "poster": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
        "synopsis": "Paul Atreides se une a los Fremen para vengar a su familia y enfrentar su destino.",
        "trailerUrl": "https://www.youtube.com/watch?v=Way9Dexny3w",
        "price": 90.0
    },
    {
        "title": "Kung Fu Panda 4",
        "genre": "Animación",
        "duration": "94 min",
        "poster": "https://image.tmdb.org/t/p/w500/kDp1vUBnMpe8ak4rjgl3cLELqjU.jpg",
        "synopsis": "Po debe encontrar y entrenar a un nuevo Guerrero Dragón.",
        "trailerUrl": "https://www.youtube.com/watch?v=_inKs4eeHiI",
        "price": 75.0
    }
]


def seed_peliculas(db: Session):
    total = db.query(Pelicula).count()

    if total > 0:
        return

    for pelicula_data in PELICULAS_INICIALES:
        pelicula = Pelicula(**pelicula_data)
        db.add(pelicula)

    db.commit()