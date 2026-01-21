<div align="center">

# 🏥 NeoCare - Sistema de Gestión Kanban

**Aplicación profesional de gestión de tareas y proyectos para equipos de salud**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?style=flat&logo=react)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-3178C6.svg?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-316192.svg?style=flat&logo=postgresql)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

[Características](#-características) •
[Requisitos](#-requisitos) •
[Instalación](#-instalación-rápida) •
[Documentación](#-documentación) •
[API](#-api-rest) •
[Despliegue](#-despliegue)

</div>

---

## 📋 Descripción

**NeoCare** es una plataforma completa de gestión de proyectos tipo Kanban desarrollada específicamente para el departamento de Innovación de NeoCare Health. El sistema permite a los equipos organizar tareas, registrar horas de trabajo y generar reportes de productividad de manera eficiente y segura.

### 🎯 Propósito del Proyecto

Facilitar la gestión ágil de proyectos mediante:
- **Tableros Kanban** personalizables por usuario
- **Registro de horas** (worklogs) con seguimiento detallado
- **Reportes semanales** automáticos con métricas de productividad
- **Autenticación segura** con JWT
- **Control de acceso** basado en ownership de recursos

---

## ✨ Características

### 🔐 Autenticación y Seguridad
- ✅ Registro y login de usuarios
- ✅ Autenticación JWT con tokens de acceso y refresh
- ✅ Hashing seguro de contraseñas con bcrypt (12 rounds)
- ✅ Control de acceso basado en ownership
- ✅ Protección contra IDOR (Insecure Direct Object Reference)
- ✅ CORS configurado y rate limiting

### 📊 Gestión de Tableros
- ✅ Creación y gestión de tableros (boards)
- ✅ Organización en listas/columnas
- ✅ Tarjetas (cards) con título, descripción y fecha límite
- ✅ Estados de tarjetas (todo, in_progress, done)
- ✅ Drag & drop para mover tarjetas

### ⏱️ Registro de Horas (Worklogs)
- ✅ Registro de horas trabajadas por tarjeta
- ✅ Validaciones de fecha y horas
- ✅ Notas descriptivas (hasta 200 caracteres)
- ✅ Consulta de horas semanales por usuario
- ✅ Auditoría con timestamps de creación y actualización

### 📈 Sistema de Reportes
- ✅ Resumen semanal de tarjetas (completadas, vencidas, nuevas)
- ✅ Horas trabajadas por usuario
- ✅ Horas trabajadas por tarjeta
- ✅ Filtrado por semana (formato ISO 8601)
- ✅ Consultas SQL optimizadas con agregaciones

### 🔍 Monitoring y Logging
- ✅ Health checks de API y base de datos
- ✅ Logging estructurado de eventos
- ✅ Auditoría de autenticación
- ✅ Métricas de tiempo de procesamiento

---

## 🏗️ Arquitectura

```
NeoCare-MVBackend/
├── backend/                    # API FastAPI
│   ├── core/                  # Configuración y utilidades
│   │   ├── config.py         # Variables de entorno
│   │   ├── security.py       # JWT y hashing
│   │   └── logging_config.py # Setup de logging
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── board.py
│   │   ├── list.py
│   │   ├── card.py
│   │   └── worklog.py
│   ├── routers/              # Endpoints de la API
│   │   ├── auth.py          # Autenticación
│   │   ├── boards.py        # CRUD tableros
│   │   ├── lists.py         # CRUD listas
│   │   ├── cards.py         # CRUD tarjetas
│   │   ├── worklogs.py      # Registro de horas
│   │   ├── reports.py       # Reportes semanales
│   │   └── health.py        # Health checks
│   ├── schemas/              # Schemas Pydantic
│   ├── alembic/              # Migraciones de BD
│   ├── main.py               # Aplicación principal
│   └── database.py           # Configuración DB
├── frontend/                  # Aplicación React
│   ├── src/
│   │   ├── api/              # Cliente HTTP
│   │   ├── components/       # Componentes React
│   │   ├── pages/            # Páginas/Vistas
│   │   ├── context/          # Context API
│   │   └── types/            # TypeScript types
│   ├── public/
│   └── package.json
├── logs/                      # Logs de aplicación
├── .env                       # Variables de entorno (no versionado)
├── env.example               # Plantilla de variables
├── requirements.txt          # Dependencias Python
├── Makefile                  # Comandos útiles
└── README.md                 # Este archivo
```

---

## 💻 Stack Tecnológico

### Backend
- **Framework:** FastAPI 0.104.1
- **ORM:** SQLAlchemy 2.0.23
- **Base de datos:** PostgreSQL 12+
- **Autenticación:** python-jose (JWT) + passlib (bcrypt)
- **Validación:** Pydantic 2.5.0
- **Migraciones:** Alembic 1.13.0
- **Servidor:** Uvicorn 0.24.0

### Frontend
- **Framework:** React 19.2.0
- **Build tool:** Vite 7.2.4
- **Lenguaje:** TypeScript 5.9.3
- **Estilos:** TailwindCSS 4.1.18
- **Routing:** React Router DOM 7.10.1
- **HTTP Client:** Axios 1.13.2
- **Iconos:** Lucide React 0.561.0
- **Drag & Drop:** @dnd-kit 6.3.1

---

## 🚀 Instalación Rápida

### Requisitos Previos

- **Python:** 3.9 o superior
- **Node.js:** 18 o superior
- **PostgreSQL:** 12 o superior
- **Git:** Para clonar el repositorio

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/melinavm22-cloud/NeoCare-MVBackend.git
cd NeoCare-MVBackend
```

### 2️⃣ Configurar Backend

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales

# Crear base de datos
createdb neocare

# Ejecutar migraciones
cd backend
alembic upgrade head
cd ..

# Iniciar servidor
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend disponible en:** [https://neocare-health-1.onrender.com/]
**Documentación API:** [https://neocare-health-1.onrender.com/docs]

### 3️⃣ Configurar Frontend

```bash
# En otra terminal
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**Frontend disponible en:** [https://neocarehealth1.vercel.app/]

### ⚡ Usar Makefile (Alternativa)

El proyecto incluye un Makefile con comandos útiles:

```bash
# Ver todos los comandos disponibles
make help

# Setup completo backend
make install && make env-setup && make setup-db

# Setup frontend
make install-frontend

# Iniciar servicios
make run-dev        # Backend en modo desarrollo
make run-frontend   # Frontend en modo desarrollo

# Limpiar archivos temporales
make clean
```

---

## 🔧 Configuración

### Variables de Entorno

Editar el archivo `.env` con las siguientes variables:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/neocare

# JWT Configuration
SECRET_KEY=tu-clave-secreta-minimo-32-caracteres-cambiar-en-produccion
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=12

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
```

⚠️ **Importante:** 
- Cambiar `SECRET_KEY` a un valor aleatorio y seguro en producción
- Usar `openssl rand -hex 32` para generar una clave segura
- Nunca compartir el archivo `.env` en el repositorio

---

## 📚 Documentación

- **[Arquitectura del Sistema](docs/ARCHITECTURE.md)** - Diseño técnico y decisiones de arquitectura
- **[Documentación de API](docs/API.md)** - Referencia completa de endpoints
- **[Guía de Despliegue](docs/DEPLOYMENT.md)** - Instrucciones para producción
- **[Backend README](backend/README_BACKEND.md)** - Documentación detallada del backend
- **[Frontend Status](frontend/FRONTEND_STATUS.md)** - Estado y características del frontend

### 📖 Swagger UI

La documentación interactiva de la API está disponible en:
- **Swagger UI:** [https://neocare-health-1.onrender.com/docs]
- **ReDoc:** [https://neocare-health-1.onrender.com/redoc]

---

## 🌐 API REST

### Endpoints Principales

#### Autenticación
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Registrar nuevo usuario | ✅ |
| POST | `/auth/login` | Login y obtener tokens | ✅ |
| POST | `/auth/refresh` | Renovar access token | ✅ |
| POST | `/auth/logout` | Logout del usuario | ✅ |
| GET | `/auth/me` | Obtener usuario actual | ✅ |

#### Boards (Tableros)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/boards/` | Listar tableros del usuario | ✅ |
| POST | `/boards/` | Crear nuevo tablero | ✅ |
| GET | `/boards/{id}` | Obtener tablero específico | ✅ |
| PUT | `/boards/{id}` | Actualizar tablero | ✅ |
| DELETE | `/boards/{id}` | Eliminar tablero | ✅ |

#### Lists (Listas/Columnas)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/lists/board/{board_id}` | Listar listas de un tablero | ✅ |
| POST | `/lists/` | Crear nueva lista | ✅ |
| PUT | `/lists/{id}` | Actualizar lista | ✅ |
| DELETE | `/lists/{id}` | Eliminar lista | ✅ |

#### Cards (Tarjetas)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/cards/` | Listar tarjetas del usuario | ✅ |
| POST | `/cards/` | Crear nueva tarjeta | ✅ |
| PUT | `/cards/{id}` | Actualizar tarjeta | ✅ |
| DELETE | `/cards/{id}` | Eliminar tarjeta | ✅ |

#### Worklogs (Registro de Horas)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/cards/{card_id}/worklogs` | Registrar horas en tarjeta | ✅ |
| GET | `/cards/{card_id}/worklogs` | Listar worklogs de tarjeta | ✅ |
| PATCH | `/worklogs/{id}` | Actualizar worklog propio | ✅ |
| DELETE | `/worklogs/{id}` | Eliminar worklog propio | ✅ |
| GET | `/users/me/worklogs?week=YYYY-WW` | Worklogs semanales del usuario | ✅ |

#### Reports (Reportes)
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/report/{board_id}/summary?week=YYYY-WW` | Resumen semanal de tarjetas | ✅ |
| GET | `/report/{board_id}/hours-by-user?week=YYYY-WW` | Horas por usuario | ✅ |
| GET | `/report/{board_id}/hours-by-card?week=YYYY-WW` | Horas por tarjeta | ✅ |

#### Health
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/health/` | Health check público | ✅ |
| GET | `/health/db` | Health check base de datos | ✅ |
| GET | `/health/metrics` | Métricas del sistema | ✅ |

### Ejemplo de Uso

```bash
# Registrar usuario
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"SecurePass123!"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"SecurePass123!"}'

# Crear tablero (con token)
curl -X POST http://localhost:8000/boards/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi Proyecto"}'
```

---

## 🧪 Testing

### Backend

```bash
# Ejecutar tests unitarios
pytest

# Con cobertura
pytest --cov=backend --cov-report=html

# Ver reporte
open htmlcov/index.html
```

### Frontend

```bash
cd frontend

# Ejecutar tests
npm test

# Tests con cobertura
npm run test:coverage
```

### Testing Manual

Pruebas manuales realizadas con:
- Thunder Client / Postman
- Swagger UI integrado
- Navegador (frontend)

**Casos probados:**
- ✅ Registro y login de usuarios
- ✅ CRUD completo de tableros, listas y tarjetas
- ✅ Registro y consulta de worklogs
- ✅ Generación de reportes semanales
- ✅ Validaciones de seguridad y ownership
- ✅ Manejo de errores y casos edge

---

## 🚢 Despliegue

### Producción

Ver **[Guía de Despliegue](docs/DEPLOYMENT.md)** para instrucciones detalladas.

#### Checklist Pre-Despliegue

- [ ] Cambiar `SECRET_KEY` a valor aleatorio fuerte
- [ ] Configurar `DATABASE_URL` con credenciales de producción
- [ ] Actualizar `CORS_ORIGINS` con dominios permitidos
- [ ] Establecer `ENVIRONMENT=production`
- [ ] Incrementar `BCRYPT_ROUNDS` a 14-16
- [ ] Configurar HTTPS obligatorio
- [ ] Implementar rate limiting robusto
- [ ] Configurar backups automáticos de BD
- [ ] Setup de monitoreo (logs, métricas)
- [ ] Ejecutar tests completos

#### Build de Producción

```bash
# Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
cd frontend
npm run build
# Los archivos están en frontend/dist/
```

#### Opciones de Hosting

- **Backend:** Render, Railway, Fly.io, AWS, GCP, Azure
- **Frontend:** Vercel, Netlify, Cloudflare Pages
- **Base de datos:** Render PostgreSQL, Supabase, AWS RDS

---

## 📊 Modelo de Datos

```sql
-- Usuarios
users
├── id (PK)
├── username
├── email (unique)
└── password_hash

-- Tableros
boards
├── id (PK)
├── title
└── user_id (FK -> users.id)

-- Listas/Columnas
lists
├── id (PK)
├── title
└── board_id (FK -> boards.id)

-- Tarjetas
cards
├── id (PK)
├── title
├── list_id (FK -> lists.id)
├── status (todo|in_progress|done)
└── order

-- Registro de horas
worklogs
├── id (PK)
├── card_id (FK -> cards.id)
├── user_id (FK -> users.id)
├── date
├── hours
├── note
├── created_at
└── updated_at
```

---

## 🔒 Seguridad

### Medidas Implementadas

1. **Autenticación robusta**
   - JWT con expiración configurable
   - Refresh tokens para renovación segura
   - Bcrypt para hashing (12 rounds mínimo)

2. **Autorización**
   - Validación de ownership en todos los recursos
   - Prevención de IDOR
   - Control de acceso basado en usuario

3. **Protecciones adicionales**
   - CORS configurado
   - Rate limiting básico
   - Validaciones con Pydantic
   - Logging de eventos de seguridad
   - Headers de seguridad en responses

### Recomendaciones para Producción

- ✅ Usar HTTPS exclusivamente
- ✅ Implementar WAF (Web Application Firewall)
- ✅ Rate limiting con Redis
- ✅ Monitoreo de intentos de autenticación
- ✅ Auditoría de accesos
- ✅ Backups encriptados
- ✅ Secrets management (Vault, AWS Secrets Manager)

---

## 📝 Logging y Auditoría

Los logs se almacenan en `logs/app_YYYYMMDD.log` e incluyen:

- ✅ Intentos de login (exitosos y fallidos)
- ✅ Registro de nuevos usuarios
- ✅ Acceso a recursos protegidos
- ✅ Errores y excepciones
- ✅ Tiempo de procesamiento de requests
- ✅ Cambios en datos sensibles

### Formato de Logs

```
2026-01-13 16:45:23 - INFO - POST /auth/login - Status: 200 - Time: 0.234s
2026-01-13 16:45:30 - INFO - GET /boards/ - Status: 200 - Time: 0.087s
2026-01-13 16:46:12 - WARNING - Failed login attempt for user: john@example.com
```

---

## 🐛 Troubleshooting

### Problemas Comunes

**Backend no inicia:**
```bash
# Verificar variables de entorno
cat .env

# Verificar conexión a PostgreSQL
psql -U postgres -d neocare

# Ver logs
tail -f logs/app_*.log
```

**Frontend no conecta con backend:**
```bash
# Verificar CORS en backend
grep CORS_ORIGINS .env

# Verificar URL de API en frontend
grep VITE_API_URL frontend/.env
```

**Errores de migración:**
```bash
# Ver estado de migraciones
cd backend
alembic current

# Revertir y volver a aplicar
alembic downgrade -1
alembic upgrade head
```

---

## 📄 Licencia

Propiedad de **NeoCare Health**. Todos los derechos reservados.

Este es un proyecto privado desarrollado para uso interno del departamento de Innovación.

---

## 👥 Equipo de Desarrollo

**Desarrollado durante el programa de prácticas profesionales**

- **Documentación y DevOps:** Pablo Techera
- **Backend:** Melina Vaccaro Martella
- **Frontend:** Melina Vaccaro Martella
- **Testing:** Melina Vaccaro Martella

---

## 📞 Soporte

Para problemas técnicos o preguntas:

1. **Revisar logs:** `logs/app_YYYYMMDD.log`
2. **Consultar documentación:** Carpeta `docs/`
3. **Contactar:** Equipo de Innovación NeoCare Health

---

## 🎯 Roadmap Futuro

- [ ] Sistema de notificaciones en tiempo real
- [ ] Etiquetas y filtros avanzados
- [ ] Comentarios en tarjetas
- [ ] Adjuntos de archivos
- [ ] Integración con calendario
- [ ] Exportación de reportes en PDF
- [ ] Dashboard de métricas avanzadas
- [ ] Modo offline con sincronización
- [ ] App móvil (React Native)

---

<div align="center">

**⭐ NeoCare - Gestión de Proyectos Inteligente ⭐**

*Desarrollado con ❤️ por el equipo de Innovación de NeoCare Health*

</div>
