from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.database import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    funcion_id = Column(Integer, nullable=False, index=True)
    estado = Column(String(30), nullable=False, default="PENDIENTE")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    asientos = relationship(
        "ReservaAsiento",
        back_populates="reserva",
        cascade="all, delete-orphan"
    )


class ReservaAsiento(Base):
    __tablename__ = "reserva_asientos"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False, index=True)
    funcion_id = Column(Integer, nullable=False, index=True)
    asiento = Column(String(10), nullable=False)

    reserva = relationship("Reserva", back_populates="asientos")

    __table_args__ = (
        UniqueConstraint("funcion_id", "asiento", name="uq_funcion_asiento"),
    )
