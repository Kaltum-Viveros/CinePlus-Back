from sqlalchemy import Column, Float, Integer, String, Text
from app.database import Base


class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    genre = Column(String(80), nullable=False, index=True)
    duration = Column(String(50), nullable=False)
    poster = Column(Text, nullable=False)
    synopsis = Column(Text, nullable=False)
    trailerUrl = Column(Text, nullable=False)
    price = Column(Float, nullable=False)