from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CouponValidationRequest(BaseModel):
    code: str
    subtotal: float = Field(..., ge=0)


class CouponValidationResponse(BaseModel):
    valid: bool
    code: str | None = None
    discount_percentage: float = Field(0, alias="discountPercentage")
    discount_amount: float = Field(0, alias="discountAmount")
    message: str

    model_config = ConfigDict(populate_by_name=True)


class CompraTicketRequest(BaseModel):
    reserva_id: int = Field(..., alias="reservaId")
    movie_id: int = Field(..., alias="movieId")
    movie_title: str = Field(..., alias="movieTitle")
    funcion_id: int = Field(..., alias="funcionId")
    date: str
    time: str
    room: str | None = None
    seats: list[str] = Field(..., min_length=1)
    price_per_ticket: float = Field(..., alias="pricePerTicket", gt=0)

    model_config = ConfigDict(populate_by_name=True)


class CompraCreate(BaseModel):
    coupon_code: str | None = Field(default=None, alias="couponCode")
    tickets: list[CompraTicketRequest] = Field(..., min_length=1)

    model_config = ConfigDict(populate_by_name=True)


class BoletoResponse(BaseModel):
    id: int
    codigo: str
    reserva_id: int = Field(..., alias="reservaId")
    movie_id: int = Field(..., alias="movieId")
    movie_title: str = Field(..., alias="movieTitle")
    funcion_id: int = Field(..., alias="funcionId")
    date: str
    time: str
    room: str | None = None
    asiento: str
    price: float

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CompraResponse(BaseModel):
    id: int
    subtotal: float
    descuento_porcentaje: float = Field(..., alias="descuentoPorcentaje")
    descuento_monto: float = Field(..., alias="descuentoMonto")
    total: float
    cupon: str | None = None
    estado: str
    fecha_compra: datetime = Field(..., alias="fechaCompra")
    boletos: list[BoletoResponse]
    contenido_txt: str = Field(..., alias="contenidoTxt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)