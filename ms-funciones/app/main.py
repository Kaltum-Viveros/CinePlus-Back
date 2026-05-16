from datetime import date

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import Funcion
from app.schemas import FuncionCreate, FuncionResponse
from app.seed import seed_funciones

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CinePlus - Microservicio de Funciones",
    description="Administra horarios, salas y fechas disponibles para cada película.",
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
        seed_funciones(db)
    finally:
        db.close()


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "ms-funciones"
    }


@app.post("/api/v1/funciones", response_model=FuncionResponse, status_code=201)
def crear_funcion(
    funcion_data: FuncionCreate,
    db: Session = Depends(get_db)
):
    funcion_existente = (
        db.query(Funcion)
        .filter(Funcion.movie_id == funcion_data.movie_id)
        .filter(Funcion.date == funcion_data.date)
        .filter(Funcion.time == funcion_data.time)
        .filter(Funcion.room == funcion_data.room)
        .first()
    )

    if funcion_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una función para esa película, fecha, hora y sala."
        )

    funcion = Funcion(**funcion_data.model_dump(by_alias=False))
    db.add(funcion)
    db.commit()
    db.refresh(funcion)

    return funcion


@app.get("/api/v1/funciones", response_model=list[FuncionResponse])
def listar_funciones(
    db: Session = Depends(get_db)
):
    return db.query(Funcion).order_by(
        Funcion.date.asc(),
        Funcion.time.asc()
    ).all()


@app.get("/api/v1/funciones/disponibles", response_model=list[FuncionResponse])
def listar_funciones_disponibles(
    movie_id: int = Query(..., alias="movieId"),
    fecha: date = Query(..., alias="date"),
    db: Session = Depends(get_db)
):
    return (
        db.query(Funcion)
        .filter(Funcion.movie_id == movie_id)
        .filter(Funcion.date == fecha)
        .filter(Funcion.available == True)
        .order_by(Funcion.time.asc())
        .all()
    )


@app.get("/api/v1/funciones/pelicula/{movie_id}", response_model=list[FuncionResponse])
def listar_funciones_por_pelicula(
    movie_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Funcion)
        .filter(Funcion.movie_id == movie_id)
        .order_by(Funcion.date.asc(), Funcion.time.asc())
        .all()
    )


@app.get("/api/v1/funciones/{funcion_id}", response_model=FuncionResponse)
def obtener_funcion_por_id(
    funcion_id: int,
    db: Session = Depends(get_db)
):
    funcion = db.query(Funcion).filter(Funcion.id == funcion_id).first()

    if not funcion:
        raise HTTPException(
            status_code=404,
            detail="Función no encontrada."
        )

    return funcion