from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ReservaCreate(BaseModel):
    funcion_id: int = Field(..., alias="funcionId")
    asientos: list[str] = Field(..., min_length=1)

    model_config = ConfigDict(
        populate_by_name=True
    )


class ReservaResponse(BaseModel):
    id: int
    funcion_id: int = Field(..., alias="funcionId")
    asientos: list[str]
    estado: str
    fecha_creacion: datetime = Field(..., alias="fechaCreacion")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class AsientosOcupadosResponse(BaseModel):
    funcion_id: int = Field(..., alias="funcionId")
    asientos_ocupados: list[str] = Field(..., alias="asientosOcupados")

    model_config = ConfigDict(
        populate_by_name=True
    )
