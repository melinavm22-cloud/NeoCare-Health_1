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
- **Auth:** JWT
- **Hosting:** Render (backend) + Vercel (frontend)


