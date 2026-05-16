import os
import uuid

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Boleto, Compra
from app.schemas import (
    BoletoResponse,
    CompraCreate,
    CompraResponse,
    CouponValidationRequest,
    CouponValidationResponse,
)

Base.metadata.create_all(bind=engine)

RESERVAS_API_URL = os.getenv(
    "RESERVAS_API_URL",
    "http://localhost:8003/api/v1"
)

VALID_COUPONS = {
    "CINE10": 10,
    "CINE20": 20,
    "PROMO15": 15,
}

app = FastAPI(
    title="CinePlus - Microservicio de Compras y Boletos",
    description="Confirma compras, calcula totales y genera boletos.",
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
        "service": "ms-compras-boletos"
    }


def calcular_descuento(coupon_code: str | None, subtotal: float):
    if not coupon_code:
        return None, 0, 0

    code = coupon_code.strip().upper()

    if code not in VALID_COUPONS:
        raise HTTPException(
            status_code=400,
            detail="Cupón no válido."
        )

    porcentaje = VALID_COUPONS[code]
    monto = round(subtotal * (porcentaje / 100), 2)

    return code, porcentaje, monto


def generar_contenido_txt(compra: Compra, boletos: list[Boleto]) -> str:
    content = "============================================\n"
    content += "     CinePlus - Confirmación de Compra\n"
    content += "============================================\n\n"
    content += f"Compra ID: {compra.id}\n"
    content += f"Fecha de compra: {compra.fecha_compra}\n"
    content += f"Estado: {compra.estado}\n\n"

    for index, boleto in enumerate(boletos, start=1):
        content += f"--- Boleto {index} ---\n"
        content += f"Código: {boleto.codigo}\n"
        content += f"Película: {boleto.movie_title}\n"
        content += f"Función ID: {boleto.funcion_id}\n"
        content += f"Fecha: {boleto.funcion_date}\n"
        content += f"Hora: {boleto.funcion_time} hrs\n"
        content += f"Sala: {boleto.room or 'No asignada'}\n"
        content += f"Asiento: {boleto.asiento}\n"
        content += f"Precio: ${boleto.price:.2f}\n\n"

    content += "--------------------------------------------\n"
    content += f"Subtotal: ${compra.subtotal:.2f}\n"

    if compra.cupon:
        content += f"Cupón aplicado: {compra.cupon}\n"
        content += f"Descuento: {compra.descuento_porcentaje:.0f}% (-${compra.descuento_monto:.2f})\n"
    else:
        content += "Cupón aplicado: NO\n"

    content += f"TOTAL: ${compra.total:.2f}\n"
    content += "--------------------------------------------\n\n"
    content += "Gracias por su compra en CinePlus.\n"

    return content


def confirmar_reserva(reserva_id: int):
    try:
        response = httpx.post(
            f"{RESERVAS_API_URL}/reservas/{reserva_id}/confirmar",
            timeout=5.0
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="No se pudo conectar con el microservicio de reservas."
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=409,
            detail=f"No se pudo confirmar la reserva {reserva_id}."
        )


def construir_respuesta(compra: Compra, boletos: list[Boleto]) -> dict:
    return {
        "id": compra.id,
        "subtotal": compra.subtotal,
        "descuento_porcentaje": compra.descuento_porcentaje,
        "descuento_monto": compra.descuento_monto,
        "total": compra.total,
        "cupon": compra.cupon,
        "estado": compra.estado,
        "fecha_compra": compra.fecha_compra,
        "boletos": [
            {
                "id": boleto.id,
                "codigo": boleto.codigo,
                "reserva_id": boleto.reserva_id,
                "movie_id": boleto.movie_id,
                "movie_title": boleto.movie_title,
                "funcion_id": boleto.funcion_id,
                "date": boleto.funcion_date,
                "time": boleto.funcion_time,
                "room": boleto.room,
                "asiento": boleto.asiento,
                "price": boleto.price,
            }
            for boleto in boletos
        ],
        "contenido_txt": generar_contenido_txt(compra, boletos)
    }


@app.post("/api/v1/cupones/validar", response_model=CouponValidationResponse)
def validar_cupon(coupon_data: CouponValidationRequest):
    code = coupon_data.code.strip().upper()

    if code not in VALID_COUPONS:
        return {
            "valid": False,
            "code": code,
            "discount_percentage": 0,
            "discount_amount": 0,
            "message": "Cupón no válido. Prueba: CINE10, CINE20 o PROMO15."
        }

    porcentaje = VALID_COUPONS[code]
    monto = round(coupon_data.subtotal * (porcentaje / 100), 2)

    return {
        "valid": True,
        "code": code,
        "discount_percentage": porcentaje,
        "discount_amount": monto,
        "message": "Cupón aplicado correctamente."
    }


@app.post("/api/v1/compras", response_model=CompraResponse, status_code=201)
def crear_compra(
    compra_data: CompraCreate,
    db: Session = Depends(get_db)
):
    tickets = compra_data.tickets

    subtotal = 0.0

    for ticket in tickets:
        subtotal += len(ticket.seats) * ticket.price_per_ticket

    subtotal = round(subtotal, 2)

    cupon, descuento_porcentaje, descuento_monto = calcular_descuento(
        compra_data.coupon_code,
        subtotal
    )

    total = round(subtotal - descuento_monto, 2)

    reserva_ids = sorted({ticket.reserva_id for ticket in tickets})

    for reserva_id in reserva_ids:
        confirmar_reserva(reserva_id)

    compra = Compra(
        subtotal=subtotal,
        descuento_porcentaje=descuento_porcentaje,
        descuento_monto=descuento_monto,
        total=total,
        cupon=cupon,
        estado="CONFIRMADA"
    )

    db.add(compra)
    db.flush()

    boletos_creados: list[Boleto] = []

    for ticket in tickets:
        for seat in ticket.seats:
            asiento = seat.strip().upper()
            codigo = f"CINE-{compra.id}-{ticket.funcion_id}-{asiento}-{uuid.uuid4().hex[:6].upper()}"

            boleto = Boleto(
                compra_id=compra.id,
                reserva_id=ticket.reserva_id,
                movie_id=ticket.movie_id,
                movie_title=ticket.movie_title,
                funcion_id=ticket.funcion_id,
                funcion_date=ticket.date,
                funcion_time=ticket.time,
                room=ticket.room,
                asiento=asiento,
                price=ticket.price_per_ticket,
                codigo=codigo
            )

            db.add(boleto)
            boletos_creados.append(boleto)

    db.commit()
    db.refresh(compra)

    for boleto in boletos_creados:
        db.refresh(boleto)

    return construir_respuesta(compra, boletos_creados)


@app.get("/api/v1/compras/{compra_id}", response_model=CompraResponse)
def obtener_compra(
    compra_id: int,
    db: Session = Depends(get_db)
):
    compra = db.query(Compra).filter(Compra.id == compra_id).first()

    if not compra:
        raise HTTPException(
            status_code=404,
            detail="Compra no encontrada."
        )

    boletos = (
        db.query(Boleto)
        .filter(Boleto.compra_id == compra_id)
        .order_by(Boleto.id.asc())
        .all()
    )

    return construir_respuesta(compra, boletos)


@app.get("/api/v1/compras/{compra_id}/boletos", response_model=list[BoletoResponse])
def obtener_boletos(
    compra_id: int,
    db: Session = Depends(get_db)
):
    boletos = (
        db.query(Boleto)
        .filter(Boleto.compra_id == compra_id)
        .order_by(Boleto.id.asc())
        .all()
    )

    if not boletos:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron boletos para esta compra."
        )

    return [
        {
            "id": boleto.id,
            "codigo": boleto.codigo,
            "reserva_id": boleto.reserva_id,
            "movie_id": boleto.movie_id,
            "movie_title": boleto.movie_title,
            "funcion_id": boleto.funcion_id,
            "date": boleto.funcion_date,
            "time": boleto.funcion_time,
            "room": boleto.room,
            "asiento": boleto.asiento,
            "price": boleto.price,
        }
        for boleto in boletos
    ]


@app.get("/api/v1/compras/{compra_id}/boletos.txt", response_class=PlainTextResponse)
def descargar_boletos_txt(
    compra_id: int,
    db: Session = Depends(get_db)
):
    compra = db.query(Compra).filter(Compra.id == compra_id).first()

    if not compra:
        raise HTTPException(
            status_code=404,
            detail="Compra no encontrada."
        )

    boletos = (
        db.query(Boleto)
        .filter(Boleto.compra_id == compra_id)
        .order_by(Boleto.id.asc())
        .all()
    )

    return generar_contenido_txt(compra, boletos)