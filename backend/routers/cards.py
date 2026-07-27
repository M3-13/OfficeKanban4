from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import Board, Card, Column, User
from backend.schemas import CardCreate, CardMove, CardResponse, CardUpdate

router = APIRouter(tags=["cards"])


def _get_card_and_verify_owner(card_id: int, user: User, db: Session) -> Card:
    card = db.query(Card).filter(Card.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    col = db.query(Column).filter(Column.id == card.column_id).first()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    board = db.query(Board).filter(Board.id == col.board_id).first()
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return card


def _get_column_and_verify_owner(column_id: int, user: User, db: Session) -> Column:
    col = db.query(Column).filter(Column.id == column_id).first()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    board = db.query(Board).filter(Board.id == col.board_id).first()
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return col


def _reposition_cards(column_id: int, db: Session) -> None:
    cards = db.query(Card).filter(Card.column_id == column_id).order_by(Card.position).all()
    for idx, card in enumerate(cards):
        card.position = idx


@router.get("/columns/{column_id}/cards", response_model=list[CardResponse])
def list_cards(
    column_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_column_and_verify_owner(column_id, user, db)
    return db.query(Card).filter(Card.column_id == column_id).order_by(Card.position).all()


@router.post(
    "/columns/{column_id}/cards",
    response_model=CardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_card(
    column_id: int,
    payload: CardCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_column_and_verify_owner(column_id, user, db)
    max_pos = (
        db.query(Card).filter(Card.column_id == column_id).order_by(Card.position.desc()).first()
    )
    next_position = (max_pos.position + 1) if max_pos and max_pos.position is not None else 0
    card = Card(
        title=payload.title,
        description=payload.description,
        position=next_position,
        column_id=column_id,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.put("/cards/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    payload: CardUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = _get_card_and_verify_owner(card_id, user, db)
    if payload.title is not None:
        card.title = payload.title
    if payload.description is not None:
        card.description = payload.description
    db.commit()
    db.refresh(card)
    return card


@router.put("/cards/{card_id}/move", response_model=CardResponse)
def move_card(
    card_id: int,
    payload: CardMove,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = _get_card_and_verify_owner(card_id, user, db)
    target_column = _get_column_and_verify_owner(payload.column_id, user, db)

    old_column_id = card.column_id
    target_position = payload.position

    if old_column_id != target_column.id:
        card.column_id = target_column.id
        db.flush()
        _reposition_cards(old_column_id, db)

    target_cards = (
        db.query(Card).filter(Card.column_id == target_column.id).order_by(Card.position).all()
    )

    target_cards = [c for c in target_cards if c.id != card.id]
    insert_at = min(target_position, len(target_cards))
    target_cards.insert(insert_at, card)

    for idx, c in enumerate(target_cards):
        c.position = idx

    db.commit()
    db.refresh(card)
    return card


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = _get_card_and_verify_owner(card_id, user, db)
    db.delete(card)
    db.commit()
    return None
