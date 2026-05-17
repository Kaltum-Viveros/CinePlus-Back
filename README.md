# 🎬 CinePlus Back

Backend basado en arquitectura de microservicios para la plataforma **CinePlus**.

Este repositorio contiene los microservicios encargados de gestionar películas, funciones, reservas de asientos, compras y boletos. La solución está preparada para ejecutarse con **Docker Compose** junto con el frontend Angular.

---

## 📁 Arquitectura general

```text
cineplus-back/
├── ms-peliculas/
├── ms-funciones/
├── ms-reservas-asientos/
├── ms-compras-boletos/
└── docker-compose.yml
```

Cada microservicio tiene su propia responsabilidad y su propia base de datos PostgreSQL.

---

## 🧩 Microservicios

### 1. `ms-peliculas`

Responsable de gestionar la cartelera disponible del cine.

**Funciones principales:**
- Registrar películas
- Consultar cartelera completa
- Consultar película por ID
- Consultar película por nombre
- Filtrar películas por género

- **Puerto local:** `http://localhost:8001`
- **Documentación Swagger:** `http://localhost:8001/docs`
- **Base de datos:** `db-peliculas` → `peliculas_db`

**Endpoints principales:**

```
GET    /api/v1/health
POST   /api/v1/peliculas
GET    /api/v1/peliculas
GET    /api/v1/peliculas/{pelicula_id}
GET    /api/v1/peliculas/buscar?title=Inception
GET    /api/v1/peliculas/genero/{genre}
```

---

### 2. `ms-funciones`

Responsable de administrar horarios, salas y fechas disponibles para cada película.

**Funciones principales:**
- Registrar funciones
- Consultar funciones
- Consultar funciones por película
- Consultar funciones disponibles por película y fecha
- Validar disponibilidad por fecha y hora

- **Puerto local:** `http://localhost:8002`
- **Documentación Swagger:** `http://localhost:8002/docs`
- **Base de datos:** `db-funciones` → `funciones_db`

**Endpoints principales:**

```
GET    /api/v1/health
POST   /api/v1/funciones
GET    /api/v1/funciones
GET    /api/v1/funciones/{funcion_id}
GET    /api/v1/funciones/pelicula/{movie_id}
GET    /api/v1/funciones/disponibles?movieId=1&date=2026-05-16
```

---

### 3. `ms-reservas-asientos`

Responsable de controlar la disponibilidad real de asientos.

**Funciones principales:**
- Consultar asientos ocupados por función
- Crear reservas
- Marcar asientos como ocupados
- Evitar doble reservación del mismo asiento

- **Puerto local:** `http://localhost:8003`
- **Documentación Swagger:** `http://localhost:8003/docs`
- **Base de datos:** `db-reservas` → `reservas_db`

**Endpoints principales:**

```
GET    /api/v1/health
GET    /api/v1/asientos/funcion/{funcion_id}
POST   /api/v1/reservas
GET    /api/v1/reservas/{reserva_id}
POST   /api/v1/reservas/{reserva_id}/confirmar
DELETE /api/v1/reservas/{reserva_id}
```

**Ejemplo de reserva:**

```json
{
  "funcionId": 1,
  "asientos": ["A1", "A2"]
}
```

---

### 4. `ms-compras-boletos`

Responsable de confirmar compras y generar boletos.

**Funciones principales:**
- Recibir una compra desde el carrito
- Validar cupones
- Calcular subtotal, descuento y total
- Confirmar reservas
- Generar boletos con códigos únicos
- Generar contenido TXT de boletos

- **Puerto local:** `http://localhost:8004`
- **Documentación Swagger:** `http://localhost:8004/docs`
- **Base de datos:** `db-compras` → `compras_db`

**Endpoints principales:**

```
GET    /api/v1/health
POST   /api/v1/cupones/validar
POST   /api/v1/compras
GET    /api/v1/compras/{compra_id}
GET    /api/v1/compras/{compra_id}/boletos
GET    /api/v1/compras/{compra_id}/boletos.txt
```

**Cupones disponibles:**

| Código    | Descuento |
|-----------|-----------|
| `CINE10`  | 10%       |
| `CINE20`  | 20%       |
| `PROMO15` | 15%       |

---

## 🌐 Frontend

El frontend Angular se ejecuta desde el repositorio `cineplus-front`, pero se orquesta desde este `docker-compose.yml`.

- **Puerto local:** `http://localhost:4200`

---

## 🔌 Puertos del sistema

| Servicio               | Puerto local | Puerto interno |
|------------------------|:------------:|:--------------:|
| `cineplus-front`       | 4200         | 80             |
| `ms-peliculas`         | 8001         | 8000           |
| `ms-funciones`         | 8002         | 8000           |
| `ms-reservas-asientos` | 8003         | 8000           |
| `ms-compras-boletos`   | 8004         | 8000           |
| `db-peliculas`         | 5433         | 5432           |
| `db-funciones`         | 5434         | 5432           |
| `db-reservas`          | 5435         | 5432           |
| `db-compras`           | 5436         | 5432           |

---

## 🚀 Ejecutar el proyecto completo

Desde la carpeta `cineplus-back`:

```bash
docker compose up -d --build
```

**Ver contenedores activos:**

```bash
docker ps
```

**Ver logs:**

```bash
docker compose logs
```

**Ver logs de un servicio específico:**

```bash
docker compose logs ms-peliculas
docker compose logs ms-funciones
docker compose logs ms-reservas-asientos
docker compose logs ms-compras-boletos
docker compose logs cineplus-front
```

**Detener contenedores:**

```bash
docker compose down
```

**Detener contenedores y borrar volúmenes de base de datos:**

```bash
docker compose down -v
```

---

## 🧪 Flujo de prueba completo

1. **Ejecutar el proyecto:**
   ```bash
   docker compose up -d --build
   ```

2. **Abrir el frontend:** `http://localhost:4200`

3. **Probar la cartelera:** la pantalla de cartelera debe cargar películas desde `ms-peliculas`.

4. Seleccionar una película y una fecha. Los horarios deben cargarse desde `ms-funciones`.

5. Seleccionar una hora. Los asientos ocupados deben consultarse desde `ms-reservas-asientos`.

6. Seleccionar asientos (ej. `A1`, `A2`) y agregar al carrito. El frontend debe crear una reserva en `ms-reservas-asientos`.

7. Volver a la misma función. Los asientos reservados deben aparecer como ocupados.

8. Ir al carrito y aplicar un cupón, por ejemplo `CINE10`.

9. **Confirmar compra:** `ms-compras-boletos` calculará el total, confirmará la reserva y generará los boletos.

10. Verificar que se descargue el archivo TXT de boletos.

---

## ⚡ Pruebas rápidas por endpoint

**Películas:**
```
GET http://localhost:8001/api/v1/peliculas
```

**Funciones disponibles** *(usar una fecha dentro de los próximos 14 días generados por el seed)*:
```
GET http://localhost:8002/api/v1/funciones/disponibles?movieId=1&date=2026-05-16
```

**Asientos ocupados:**
```
GET http://localhost:8003/api/v1/asientos/funcion/1
```

**Validar cupón:**
```bash
curl -X POST http://localhost:8004/api/v1/cupones/validar \
  -H "Content-Type: application/json" \
  -d '{"code":"CINE10","subtotal":200}'
```

**Crear reserva:**
```bash
curl -X POST http://localhost:8003/api/v1/reservas \
  -H "Content-Type: application/json" \
  -d '{"funcionId":1,"asientos":["A1","A2"]}'
```

---

## 🛠️ Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [Angular](https://angular.io/)
- [Nginx](https://nginx.org/)

---

## 📝 Notas importantes

- Cada microservicio tiene su propia base de datos.
- Los microservicios exponen endpoints REST.
- El frontend consume los microservicios mediante HTTP.
- La disponibilidad de asientos ya no depende de `localStorage`.
- Las compras y boletos son generados por el backend.
- El sistema completo se puede levantar con Docker Compose.