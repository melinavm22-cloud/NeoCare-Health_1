from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, boards, cards, lists, health, worklogs, reports
from .core.config import Base, engine, CORS_ORIGINS
from .models import user, board, list, card, worklog
from .core.logging_config import setup_logging
import logging
import time
import os

# Configurar logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logger = setup_logging()

app = FastAPI(title="NeoCare Backend API", version="1.0.0")

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Procesar request
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    
    # Log de la request
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    # Agregar header con tiempo de procesamiento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Registrar los routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(boards.router)
app.include_router(lists.router)
app.include_router(cards.router)
app.include_router(worklogs.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {"message": "NeoCare Backend funcionando"}
