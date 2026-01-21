# NeoCare Frontend - Estado del Proyecto

##  Resumen

Frontend completo para la aplicación NeoCare, implementado con React + Vite + TypeScript + TailwindCSS.

**Fecha:** 16 de Diciembre 2025

---

##  Funcionalidades Implementadas

### Autenticación
- [x] Página de Login
- [x] Página de Registro
- [x] Manejo de token JWT
- [x] Rutas protegidas
- [x] Logout

### Dashboard
- [x] Listado de tableros del usuario
- [x] Crear nuevo tablero
- [x] Navegación a vista de tablero

### Vista de Tablero (Kanban)
- [x] Columnas/Listas
- [x] Crear nueva lista
- [x] Tarjetas por columna

### Tarjetas (Cards)
- [x] Mostrar tarjetas por columnas
- [x] Crear tarjeta (título, descripción, fecha límite)
- [x] Editar tarjeta
- [x] Eliminar tarjeta
- [x] Validaciones:
  - Título requerido (1-80 caracteres)
  - Fecha límite válida
- [x] Renderizado con:
  - Título
  - Estado (pendiente, en progreso, completado)
  - Badge de fecha límite (vencida, hoy, mañana, próximos días)

### Manejo de Errores
- [x] Mensajes de error visuales
- [x] Validaciones en formularios

---

##  Credenciales de Prueba

```
URL: https://neocarehealth1.vercel.app/
Email: admin@neocare.com
Password: R7M2K9T4B8Q1
```
El frontend estará disponible en `[https://neocarehealth1.vercel.app/]`

---

##  Estructura del Proyecto

```
src/
├── api/
│   ├── axios.ts       # Cliente HTTP con interceptores JWT
│   ├── auth.ts        # Login, register, getMe
│   ├── boards.ts      # CRUD tableros
│   ├── lists.ts       # CRUD listas
│   └── cards.ts       # CRUD tarjetas
├── components/
│   ├── CardItem.tsx       # Componente tarjeta
│   ├── CardModal.tsx      # Modal crear/editar tarjeta
│   └── ProtectedRoute.tsx # Wrapper rutas protegidas
├── context/
│   └── AuthContext.tsx    # Contexto de autenticación
├── pages/
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   └── BoardView.tsx      # Vista Kanban
├── types/
│   └── index.ts
├── App.tsx
├── main.tsx
└── index.css
```

---

##  Pendiente para Backend

El frontend actualmente funciona con **datos mock**. Para conectar con el backend real:

### 1. Agregar CORS en el backend

En `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Implementar endpoints de Lists

| Método | Endpoint | Body | Descripción |
|--------|----------|------|-------------|
| GET | `/lists?board_id={id}` | - | Listar listas de un tablero |
| POST | `/lists/` | `{title, board_id}` | Crear lista |
| DELETE | `/lists/{id}` | - | Eliminar lista |

### 3. Implementar endpoints de Cards

| Método | Endpoint | Body | Descripción |
|--------|----------|------|-------------|
| GET | `/cards?board_id={id}` | - | Listar tarjetas de un tablero |
| POST | `/cards/` | `{title, description?, due_date?, list_id, board_id}` | Crear tarjeta |
| PUT | `/cards/{id}` | `{title?, description?, due_date?, status?, list_id?}` | Editar tarjeta |
| DELETE | `/cards/{id}` | - | Eliminar tarjeta |

### 4. Modelo Card sugerido

```python
class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, in_progress, done
    list_id = Column(Integer, ForeignKey("lists.id"))
    board_id = Column(Integer, ForeignKey("boards.id"))
```
##  Tecnologías

- React 19
- Vite 7
- TypeScript
- TailwindCSS 4
- React Router DOM 7
- Axios
- Lucide React (iconos)

---

##  Contacto

Cualquier duda sobre el frontend, preguntar en el canal de Slack.
