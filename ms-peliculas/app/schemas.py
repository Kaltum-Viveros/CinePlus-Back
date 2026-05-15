from pydantic import BaseModel, Field


class PeliculaBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    genre: str = Field(..., min_length=1, max_length=80)
    duration: str = Field(..., min_length=1, max_length=50)
    poster: str
    synopsis: str
    trailerUrl: str
    price: float = Field(..., gt=0)


class PeliculaCreate(PeliculaBase):
    pass


class PeliculaResponse(PeliculaBase):
    id: int

    class Config:
        from_attributes = True