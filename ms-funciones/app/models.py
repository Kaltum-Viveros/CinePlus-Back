from sqlalchemy import Boolean, Column, Date, Integer, String
from app.database import Base


class Funcion(Base):
    __tablename__ = "funciones"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, nullable=False, index=True)
    movie_title = Column(String(150), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(String(10), nullable=False)
    room = Column(String(30), nullable=False)
    available = Column(Boolean, default=True, nullable=False)