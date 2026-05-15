from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import Pelicula
from app.schemas import PeliculaCreate, PeliculaResponse
from app.seed import seed_peliculas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CinePlus - Microservicio de Películas",
    description="Gestiona la cartelera disponible del cine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_peliculas(db)
    finally:
        db.close()


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "ms-peliculas"
    }


@app.post("/api/v1/peliculas", response_model=PeliculaResponse, status_code=201)
def crear_pelicula(
    pelicula_data: PeliculaCreate,
    db: Session = Depends(get_db)
):
    pelicula_existente = (
        db.query(Pelicula)
        .filter(Pelicula.title.ilike(pelicula_data.title))
        .first()
    )

    if pelicula_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una película con ese nombre."
        )

    pelicula = Pelicula(**pelicula_data.model_dump())
    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)

    return pelicula


@app.get("/api/v1/peliculas", response_model=list[PeliculaResponse])
def listar_peliculas(
    genre: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Pelicula)

    if genre:
        query = query.filter(Pelicula.genre.ilike(f"%{genre}%"))

    return query.order_by(Pelicula.id.asc()).all()


@app.get("/api/v1/peliculas/buscar", response_model=list[PeliculaResponse])
def buscar_pelicula_por_nombre(
    title: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    return (
        db.query(Pelicula)
        .filter(Pelicula.title.ilike(f"%{title}%"))
        .order_by(Pelicula.id.asc())
        .all()
    )


@app.get("/api/v1/peliculas/genero/{genre}", response_model=list[PeliculaResponse])
def filtrar_peliculas_por_genero(
    genre: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Pelicula)
        .filter(Pelicula.genre.ilike(f"%{genre}%"))
        .order_by(Pelicula.id.asc())
        .all()
    )


@app.get("/api/v1/peliculas/{pelicula_id}", response_model=PeliculaResponse)
def obtener_pelicula_por_id(
    pelicula_id: int,
    db: Session = Depends(get_db)
):
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()

    if not pelicula:
        raise HTTPException(
            status_code=404,
            detail="Película no encontrada."
        )

    return pelicula