# NeoCare - Monorepo

Aplicación de gestión de tareas tipo Kanban.

##  Estructura

```
NeoCare-MVBackend/
├── backend/         # API FastAPI + PostgreSQL
├── frontend/        # React + Vite + TypeScript
└── README.md
```

##  Cómo ejecutar

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
URL: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
URL: http://localhost:5173

**Credenciales de prueba (modo mock):**
- Email: `admin@neocare.com`
- Password: `admin123`

##  Documentación

- **Frontend:** Ver `frontend/FRONTEND_STATUS.md`
- **Backend:** Ver notas en `backend/README.md`

## Tecnologías

- **Backend:** Python + FastAPI + PostgreSQL
- **Frontend:** React + Vite + TypeScript + TailwindCSS

# NeoCare - Monorepo

Aplicación de gestión de tareas tipo Kanban desarrollada para el departamento de Innovación de NeoCare Health.  
El sistema permite autenticación de usuarios, gestión de tableros y manejo de tarjetas (cards) como unidades mínimas de trabajo.

El proyecto utiliza una arquitectura tipo monorepo con backend en FastAPI y frontend en React.

---

## 🗂 Backend (FastAPI)

### Tecnologías
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### Modelos principales
- User
- Board
- List
- Card

---

## 📝 Modelo Card

Una tarjeta representa una tarea dentro del tablero Kanban.

### Campos

| Campo | Tipo | Descripción |
|-----|-----|------------|
| id | integer | Identificador único |
| board_id | integer | Tablero al que pertenece |
| list_id | integer | Columna actual |
| title | varchar(80) | Título de la tarjeta |
| description | text | Descripción opcional |
| due_date | date | Fecha límite |
| user_id | integer | Usuario creador |
| created_at | timestamp | Fecha de creación |
| updated_at | timestamp | Última actualización |

---

## 🔗 Endpoints — Cards

### Crear tarjeta
## POST/CARDS


**Body**
```json
{
  "title": "Implementar login",
  "list_id": 1
}

#Listar Tarjetas

#GET /cards

#Ver tarjetas por ID
##GET /cards/{id}

Actualizar tarjeta
##PUT /cards/{id}

##Eliminar tarjeta
#DELETE /cards/{id}

"""rontend (React)
 Estado actual:
El frontend se genera mediante un script automatizado (generate_frontend.py).

Este script crea una aplicación React con:

Autenticación (login y register)
Manejo de JWT
Rutas protegidas
Dashboard
Vista de tableros
Interfaz Kanban base

Tecnologías

React 18
React Router DOM
Axios
Bootstrap
"""
##Configuracion Frontend

REACT_APP_API_URL=http://localhost:8000

##Ejecucion del proyecto

##cd backend
uvicorn main:app --reload

##Frontend

python generate_frontend.py

##Entrar al Frontend

```
cd NeoCare-MVFrontend
npm install
npm start
```

##Testing

#Pruebas manuales realizadas con Thunder Client / Postman para verificar:

Login
Creación de tarjetas
Listado de tarjetas
Edición de tarjetas
Manejo de errores de la API



- **Auth:** JWT
- **Hosting:** Render (backend) + Vercel (frontend)


# Semana 4

## Nueva tabla worklogs

|  Campo     |     Tipo	     |          Descripción         |
|   id	     |  SERIAL PK	   |  Identificador del worklog   |
| card_id	   |  INTEGER FK	 |  Tarjeta asociada            |
| user_id	   |  INTEGER FK	 |  Usuario autor del registro  |
| date		   |  DATE		     |  Fecha del registro          |
| hours		   |  FLOAT		     |  Horas dedicadas (> 0)       |
| note		   |  VARCHAR(200) |  Nota opcional               |
| created_at |  TIMESTAMP	   |  Fecha de creación           |
| updated_at |  TIMESTAMP	   |  Fecha de actualización      |



## Endpoints creados

### Proceso worlogs para crear
POST /cards/{card_id}/worklogs

### Para listar worklogs por tarjeta
GET /cards/{card_id}/worklogs

### Para editar worklog propio
PATCH /worklogs/{id}

### Para eliminar worklog propio
DELETE /worklogs/{id}

### Para obtener worklogs semanales del usuario autenticado
GET /users/me/worklogs?week=YYYY-WW


## Validaciones de cliente + servidor

### Backend
hours > 0 (mínimo recomendado: 0.25)
date válida y no futura
note ≤ 200 caracteres
Solo el autor puede editar o eliminar su worklog
JWT obligatorio
Acceso restringido a tarjetas del equipo

### Frontend
Validar horas > 0
Validar fecha válida
Validar longitud de nota
Mostrar errores del servidor
Refrescar la tarjeta tras crear/editar/eliminar


## Ejemplos de payload

### Para Crear worklog
{
  "date": "2025-01-20",
  "hours": 2.5,
  "note": "Revisión de endpoints"
}

### Para editar worklog
{
  "hours": 3,
  "note": "Ajuste tras pruebas"
}

### Para respuesta de listado por tarjeta
[
  {
    "id": 18,
    "card_id": 42,
    "user_id": 7,
    "date": "2025-01-20",
    "hours": 2.5,
    "note": "Revisión de endpoints",
    "created_at": "2025-01-20T10:15:00",
    "updated_at": "2025-01-20T10:15:00"
  }
]

### Para respuesta semanal (usuario actual)
{
  "week": "2025-04",
  "total_week_hours": 12.5,
  "daily_totals": {
    "2025-01-20": 4.0,
    "2025-01-21": 3.5,
    "2025-01-22": 5.0
  },
  "worklogs": [...]
}
