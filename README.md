\# CinePlus Back



Backend basado en microservicios para la plataforma CinePlus.



\## Microservicios planeados



\### 1. ms-peliculas



Responsable de gestionar la cartelera del cine.



Funciones principales:



\- Registrar películas.

\- Consultar cartelera completa.

\- Consultar película por nombre.

\- Filtrar películas por género.



\### 2. ms-funciones



Responsable de administrar horarios, fechas y salas disponibles para cada película.



Funciones principales:



\- Registrar funciones.

\- Consultar funciones por película.

\- Validar disponibilidad por fecha y hora.



\### 3. ms-reservas-asientos



Responsable de controlar la disponibilidad de asientos.



Funciones principales:



\- Consultar asientos ocupados por función.

\- Crear reservas.

\- Evitar doble reservación del mismo asiento.



\### 4. ms-compras-boletos



Responsable de confirmar compras y generar boletos.



Funciones principales:



\- Recibir compra desde el carrito.

\- Calcular subtotal, descuentos y total.

\- Generar boletos.



\## Tecnologías propuestas



\- FastAPI

\- PostgreSQL

\- Docker

\- Docker Compose

\- API REST



\## Estructura inicial



```text

cineplus-back/

├── ms-peliculas/

├── ms-funciones/

├── ms-reservas-asientos/

├── ms-compras-boletos/

├── .gitignore

└── README.md

