from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.config import get_db
from backend.models.card import Card
from backend.models.list import List
from backend.models.board import Board
from backend.models.user import User
from backend.routers.auth import get_current_user
from backend.schemas.card import CardCreate, CardUpdate, CardOut

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

# Crear tarjeta
@router.post("/", response_model=CardOut)
def create_card(card_data: CardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar que la lista pertenece a un board del usuario
    list_obj = db.query(List).filter(List.id == card_data.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board or board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear tarjetas en esta lista")
    
    card = Card(
        title=card_data.title,
        list_id=card_data.list_id,
        status="todo",
        order=0
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

# Listar tarjetas del usuario autenticado
@router.get("/", response_model=list[CardOut])
def read_cards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Obtener solo las tarjetas de boards que pertenecen al usuario
    cards = (
        db.query(Card)
        .join(List, Card.list_id == List.id)
        .join(Board, List.board_id == Board.id)
        .filter(Board.user_id == current_user.id)
        .all()
    )
    return cards

# Actualizar tarjeta
@router.put("/{card_id}", response_model=CardOut)
def update_card(card_id: int, card_data: CardUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    # Validar ownership a través de list -> board
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board or board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta tarjeta")
    
    # Si se cambia de lista, validar que la nueva lista también pertenece al usuario
    if card_data.list_id is not None and card_data.list_id != card.list_id:
        new_list = db.query(List).filter(List.id == card_data.list_id).first()
        if not new_list:
            raise HTTPException(status_code=404, detail="Nueva lista no encontrada")
        
        new_board = db.query(Board).filter(Board.id == new_list.board_id).first()
        if not new_board or new_board.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tienes permiso para mover la tarjeta a esta lista")
        
        card.list_id = card_data.list_id
    
    # Actualizar campos simples
    if card_data.title is not None:
        card.title = card_data.title
    if card_data.status is not None:
        card.status = card_data.status
    
    # Lógica de orden
    if card_data.order is not None:
        cards_in_list = (
            db.query(Card)
            .filter(Card.list_id == card.list_id, Card.id != card.id)
            .order_by(Card.order)
            .all()
        )
        
        new_order = card_data.order
        cards_in_list.insert(new_order, card)
        
        for idx, c in enumerate(cards_in_list):
            c.order = idx
    
    db.commit()
    db.refresh(card)
    return card

# Eliminar tarjeta
@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    # Validar ownership
    list_obj = db.query(List).filter(List.id == card.list_id).first()
    if not list_obj:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    board = db.query(Board).filter(Board.id == list_obj.board_id).first()
    if not board or board.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta tarjeta")
    
    db.delete(card)
    db.commit()
    return {"detail": "Tarjeta eliminada"}

