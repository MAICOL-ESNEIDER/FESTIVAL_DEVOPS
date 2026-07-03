# 🎪 Festival DevOps Music Fest

Proyecto integrador del programa **DevOps y Contenedores (Docker)** — SENA CTMA.
Landing page de un festival musical con backend en Flask, base de datos MySQL,
todo containerizado con Docker y orquestado con Docker Compose, versionado con
Git Flow y publicado en GitHub.

## 🧱 Arquitectura

```
Usuario
  │
Frontend (HTML / CSS / JS)  →  Nginx
  │
Backend (Python Flask)      →  API REST
  │
Base de datos MySQL 8.0
  │
Docker Compose (orquesta los 3 servicios + red + volumen)
  │
Git y GitHub (control de versiones)
```

## 🛠️ Tecnologías utilizadas

| Categoría          | Tecnología                                  |
|---------------------|----------------------------------------------|
| Frontend            | HTML5, CSS3, JavaScript (Fetch API)          |
| Backend             | Python 3.11, Flask, Flask-CORS               |
| Base de datos       | MySQL 8.0                                    |
| Contenedores        | Docker, Docker Compose                       |
| Servidor web        | Nginx (alpine)                               |
| Control de versiones| Git y GitHub (Git Flow)                      |

## 📁 Estructura del proyecto

```
festival-devops/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── Dockerfile
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Cómo ejecutar el proyecto

1. Clona el repositorio y entra a la carpeta:
   ```bash
   git clone https://github.com/MAICOL-ESNEIDER/FESTIVAL_DEVOPS.git
   cd FESTIVAL_DEVOPS
   ```
2. Crea tu archivo de variables de entorno a partir del ejemplo:
   ```bash
   cp .env.example .env
   ```
3. Levanta todos los servicios:
   ```bash
   docker compose up -d --build
   ```
4. Abre la aplicación:
   - Frontend: http://localhost:8080
   - Backend (API): http://localhost:5000/api/health

## 🔌 Endpoints de la API

| Método | Ruta            | Descripción                                   |
|--------|-----------------|------------------------------------------------|
| GET    | /api/health     | Verifica que el backend esté activo            |
| GET    | /api/concert    | Información general del festival               |
| GET    | /api/artists    | Lista de artistas invitados                     |
| GET    | /api/tickets    | Tipos de boletería y precios                    |
| POST   | /api/contact    | Recibe mensajes del formulario de contacto      |

## 🌿 Flujo de trabajo con Git (Git Flow básico)

El proyecto se construyó siguiendo un flujo de ramas por funcionalidad:

- `main` → rama principal, siempre estable.
- `feature-landing` → landing page (HTML/CSS).
- `feature-backend` → API en Flask.
- `feature-artistas` → sección de artistas con tarjetas dinámicas (`/api/artists`).
- `feature-tickets` → sección de tickets con precios (`/api/tickets`).
- `feature-contacto` → formulario de contacto (`/api/contact`).

Cada rama fue fusionada a `main` mediante `git merge` una vez validada,
manteniendo un historial de commits descriptivo y trazable.

## 👤 Autor

Maicol Esneider — Aprendiz ADSO, SENA CTMA
Programa: DevOps y Contenedores (Docker)
