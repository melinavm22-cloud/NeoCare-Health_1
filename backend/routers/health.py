from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.config import get_db, ENVIRONMENT
from backend.models.user import User
from backend.routers.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    """Health check público para balanceadores de carga"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": ENVIRONMENT
    }

@router.get("/db")
def health_check_db(db: Session = Depends(get_db)):
    """Health check de base de datos (público)"""
    try:
        # Ejecutar query simple para verificar conexión
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")

@router.get("/metrics")
def get_metrics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Métricas básicas protegidas (requiere autenticación)"""
    from backend.models.board import Board
    from backend.models.list import List
    from backend.models.card import Card
    
    total_users = db.query(User).count()
    total_boards = db.query(Board).count()
    total_lists = db.query(List).count()
    total_cards = db.query(Card).count()
    
    user_boards = db.query(Board).filter(Board.user_id == current_user.id).count()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "total_users": total_users,
            "total_boards": total_boards,
            "total_lists": total_lists,
            "total_cards": total_cards
        },
        "user": {
            "id": current_user.id,
            "boards_count": user_boards
        }
    }
