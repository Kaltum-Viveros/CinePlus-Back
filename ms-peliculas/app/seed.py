from sqlalchemy.orm import Session
from app.models import Pelicula


PELICULAS_INICIALES = [
    {
        "title": 'Inception',
        "genre": 'Ciencia Ficción',
        "duration": '148 min',
        "poster": 'https://image.tmdb.org/t/p/w500/ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg',
        "synopsis": 'Un ladrón que roba secretos corporativos a través del uso de la tecnología de sueños compartidos, recibe la tarea inversa de plantar una idea en la mente de un CEO.',
        "trailerUrl": 'https://www.youtube.com/embed/YoHD9XEInc0',
        "price": 80,
    },
    {
        "title": 'The Dark Knight',
        "genre": 'Acción',
        "duration": '152 min',
        "poster": 'https://image.tmdb.org/t/p/original/xQPgyZOBhaz1GdCQIPf5A5VeFzO.jpg',
        "synopsis": 'Batman se enfrenta al Joker, un criminal anárquico que desata el caos y la destrucción en Gotham City.',
        "trailerUrl": 'https://www.youtube.com/embed/EXeTwQWrcwY',
        "price": 80,
    },
    {
        "title": 'Interstellar',
        "genre": 'Ciencia Ficción',
        "duration": '169 min',
        "poster": 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
        "synopsis": 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en un intento de asegurar la supervivencia de la humanidad.',
        "trailerUrl": 'https://www.youtube.com/embed/zSWdZVtXT7E',
        "price": 85,
    },
    {
        "title": 'Spider-Man: No Way Home',
        "genre": 'Acción',
        "duration": '148 min',
        "poster": 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg',
        "synopsis": 'Con la identidad de Spider-Man revelada, Peter busca la ayuda del Doctor Strange para restaurar su secreto, desatando una crisis multiversal.',
        "trailerUrl": 'https://www.youtube.com/embed/JfVOs4VSpmA',
        "price": 90,
    },
    {
        "title": 'Coco',
        "genre": 'Animación',
        "duration": '105 min',
        "poster": 'https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg',
        "synopsis": 'Miguel sueña con ser músico y se encuentra en la Tierra de los Muertos, donde busca a su tatarabuelo para que lo ayude a cumplir su sueño.',
        "trailerUrl": 'https://www.youtube.com/embed/Rvr68u6k5sI',
        "price": 70,
    },
    {
        "title": 'The Conjuring',
        "genre": 'Terror',
        "duration": '112 min',
        "poster": 'https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg',
        "synopsis": 'Los investigadores paranormales Ed y Lorraine Warren ayudan a una familia aterrorizada por una presencia oscura en su granja.',
        "trailerUrl": 'https://www.youtube.com/embed/k10ETZ41q5o',
        "price": 75,
    },
    {
        "title": 'Toy Story 4',
        "genre": 'Animación',
        "duration": '100 min',
        "poster": 'https://image.tmdb.org/t/p/w500/w9kR8qbmQ01HwnvK4alvnQ2ca0L.jpg',
        "synopsis": 'Woody y sus amigos emprenden un viaje por carretera con Bonnie y un nuevo juguete llamado Forky, que se resiste a ser un juguete.',
        "trailerUrl": 'https://www.youtube.com/embed/wmiIUN-7qhE',
        "price": 70,
    },
    {
        "title": 'Dune',
        "genre": 'Ciencia Ficción',
        "duration": '155 min',
        "poster": 'https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg',
        "synopsis": 'Paul Atreides, un joven brillante destinado a un gran destino, viaja al planeta más peligroso del universo para asegurar el futuro de su familia.',
        "trailerUrl": 'https://www.youtube.com/embed/n9xhJrPXop4',
        "price": 90,
    },
    {
        "title": 'Avengers: Endgame',
        "genre": 'Acción',
        "duration": '181 min',
        "poster": 'https://image.tmdb.org/t/p/original/br6krBFpaYmCSglLBWRuhui7tPc.jpg',
        "synopsis": 'Los Vengadores restantes deben encontrar una manera de recuperar a sus aliados para un enfrentamiento épico contra Thanos.',
        "trailerUrl": 'https://www.youtube.com/embed/TcMBFSGVi1c',
        "price": 90,
    },
    {
        "title": 'The Notebook',
        "genre": 'Romance',
        "duration": '123 min',
        "poster": 'https://image.tmdb.org/t/p/w500/rNzQyW4f8B8cQeg7Dgj3n6eT5k9.jpg',
        "synopsis": 'Una historia de amor épica centrada en una joven pareja que se enamora durante un verano de los años 40, contada a través de un anciano que lee su historia.',
        "trailerUrl": 'https://www.youtube.com/embed/yDJIcYE32NU',
        "price": 70,
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