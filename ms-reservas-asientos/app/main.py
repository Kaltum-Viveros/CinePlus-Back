from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Reserva, ReservaAsiento
from app.schemas import AsientosOcupadosResponse, ReservaCreate, ReservaResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CinePlus - Microservicio de Reservas y Asientos",
    description="Controla la disponibilidad real de asientos y evita doble reservación.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "ms-reservas-asientos"
    }


@app.get(
    "/api/v1/asientos/funcion/{funcion_id}",
    response_model=AsientosOcupadosResponse
)
def obtener_asientos_ocupados(
    funcion_id: int,
    db: Session = Depends(get_db)
):
    asientos = (
        db.query(ReservaAsiento)
        .filter(ReservaAsiento.funcion_id == funcion_id)
        .order_by(ReservaAsiento.asiento.asc())
        .all()
    )

    return {
        "funcion_id": funcion_id,
        "asientos_ocupados": [item.asiento for item in asientos]
    }


@app.post("/api/v1/reservas", response_model=ReservaResponse, status_code=201)
def crear_reserva(
    reserva_data: ReservaCreate,
    db: Session = Depends(get_db)
):
    asientos_limpios = [
        asiento.strip().upper()
        for asiento in reserva_data.asientos
        if asiento.strip()
    ]

    if not asientos_limpios:
        raise HTTPException(
            status_code=400,
            detail="Debes seleccionar al menos un asiento."
        )

    if len(asientos_limpios) != len(set(asientos_limpios)):
        raise HTTPException(
            status_code=400,
            detail="La solicitud contiene asientos repetidos."
        )

    asientos_ocupados = (
        db.query(ReservaAsiento)
        .filter(ReservaAsiento.funcion_id == reserva_data.funcion_id)
        .filter(ReservaAsiento.asiento.in_(asientos_limpios))
        .all()
    )

    if asientos_ocupados:
        ocupados = [item.asiento for item in asientos_ocupados]
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Uno o más asientos ya están ocupados.",
                "asientosOcupados": ocupados
            }
        )

    reserva = Reserva(
        funcion_id=reserva_data.funcion_id,
        estado="PENDIENTE"
    )

    db.add(reserva)
    db.flush()

    for asiento in asientos_limpios:
        db.add(
            ReservaAsiento(
                reserva_id=reserva.id,
                funcion_id=reserva_data.funcion_id,
                asiento=asiento
            )
        )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Uno o más asientos fueron reservados por otro usuario."
        )

    db.refresh(reserva)

    return {
        "id": reserva.id,
        "funcion_id": reserva.funcion_id,
        "asientos": asientos_limpios,
        "estado": reserva.estado,
        "fecha_creacion": reserva.fecha_creacion
    }


@app.get("/api/v1/reservas/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada."
        )

    return {
        "id": reserva.id,
        "funcion_id": reserva.funcion_id,
        "asientos": [item.asiento for item in reserva.asientos],
        "estado": reserva.estado,
        "fecha_creacion": reserva.fecha_creacion
    }


@app.post("/api/v1/reservas/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada."
        )

    if reserva.estado == "CANCELADA":
        raise HTTPException(
            status_code=409,
            detail="No se puede confirmar una reserva cancelada."
        )

    reserva.estado = "CONFIRMADA"
    db.commit()
    db.refresh(reserva)

    return {
        "id": reserva.id,
        "funcion_id": reserva.funcion_id,
        "asientos": [item.asiento for item in reserva.asientos],
        "estado": reserva.estado,
        "fecha_creacion": reserva.fecha_creacion
    }


@app.delete("/api/v1/reservas/{reserva_id}")
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada."
        )

    db.query(ReservaAsiento).filter(
        ReservaAsiento.reserva_id == reserva_id
    ).delete(synchronize_session=False)

    reserva.estado = "CANCELADA"
    db.commit()

    return {
        "message": "Reserva cancelada correctamente.",
        "reservaId": reserva_id
    }