from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class FuncionBase(BaseModel):
    movie_id: int = Field(..., alias="movieId")
    movie_title: str = Field(..., alias="movieTitle")
    date: date
    time: str
    room: str
    available: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class FuncionCreate(FuncionBase):
    pass


class FuncionResponse(FuncionBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )