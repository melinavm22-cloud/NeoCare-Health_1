from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.config import get_db
from backend.models.board import Board
from backend.models.user import User
from backend.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/boards", tags=["boards"])

# --- Schemas ---
class BoardCreate(BaseModel):
    title: str

class BoardUpdate(BaseModel):
    title: str

class BoardOut(BaseModel):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True

# --- Endpoints ---
@router.post("/", response_model=BoardOut)
def create_board(board: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_board = Board(title=board.title, user_id=current_user.id)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@router.get("/", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    boards = db.query(Board).filter(Board.user_id == current_user.id).all()
    return boards

@router.get("/{board_id}", response_model=BoardOut)
def get_board(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")
    
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este board")
    
    return board

@router.put("/{board_id}", response_model=BoardOut)
def update_board(board_id: int, board_data: BoardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")
    
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este board")
    
    board.title = board_data.title
    db.commit()
    db.refresh(board)
    return board

@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")
    
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este board")
    
    db.delete(board)
    db.commit()
    return {"detail": "Board eliminado"}
