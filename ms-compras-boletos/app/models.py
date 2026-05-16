from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    subtotal = Column(Float, nullable=False)
    descuento_porcentaje = Column(Float, nullable=False, default=0)
    descuento_monto = Column(Float, nullable=False, default=0)
    total = Column(Float, nullable=False)
    cupon = Column(String(30), nullable=True)
    estado = Column(String(30), nullable=False, default="CONFIRMADA")
    fecha_compra = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    boletos = relationship(
        "Boleto",
        back_populates="compra",
        cascade="all, delete-orphan"
    )


class Boleto(Base):
    __tablename__ = "boletos"

    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False, index=True)
    reserva_id = Column(Integer, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False)
    movie_title = Column(String(150), nullable=False)
    funcion_id = Column(Integer, nullable=False, index=True)
    funcion_date = Column(String(20), nullable=False)
    funcion_time = Column(String(10), nullable=False)
    room = Column(String(30), nullable=True)
    asiento = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    codigo = Column(String(80), nullable=False, unique=True, index=True)

    compra = relationship("Compra", back_populates="boletos")