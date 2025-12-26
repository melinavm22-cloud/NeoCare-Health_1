from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.config import get_db
from backend.models.list import List
from backend.models.board import Board
from backend.models.user import User
from backend.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/lists", tags=["lists"])

# --- Schemas ---
class ListCreate(BaseModel):
    title: str
    board_id: int

class ListUpdate(BaseModel):
    title: str

class ListOut(BaseModel):
    id: int
    title: str
    board_id: int

    class Config:
        orm_mode = True

# --- Endpoints ---
@router.post("/", response_model=ListOut)
def create_list(list_data: ListCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar que el board pertenece al usuario
    board = db.query(Board).filter(Board.id == list_data.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")
    
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear listas en este board")
    
    new_list = List(title=list_data.title, board_id=list_data.board_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

@router.get("/board/{board_id}", response_model=list[ListOut])
def get_lists_by_board(board_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar que el board pertenece al usuario
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado")
    
    if board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este board")
    
    lists = db.query(List).filter(List.board_id == board_id).all()
    return lists

@router.put("/{list_id}", response_model=ListOut)
def update_list(list_id: int, list_data: ListUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    # Validar ownership a través del board
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board or board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta lista")
    
    list_obj.title = list_data.title
    db.commit()
    db.refresh(list_obj)
    return list_obj

@router.delete("/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    list_obj = db.query(List).filter(List.id == list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    # Validar ownership
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board or board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta lista")
    
    db.delete(list_obj)
    db.commit()
    return {"detail": "Lista eliminada"}
