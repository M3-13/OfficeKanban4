from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db
from backend.models import Board, Column, User
from backend.schemas import ColumnCreate, ColumnResponse, ColumnUpdate

router = APIRouter(prefix="/boards/{board_id}/columns", tags=["columns"])


def _get_board_or_403(board_id: int, user: User, db: Session) -> Board:
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    if board.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return board


@router.get("", response_model=list[ColumnResponse])
def list_columns(
    board_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_board_or_403(board_id, user, db)
    return db.query(Column).filter(Column.board_id == board_id).order_by(Column.position).all()


@router.post("", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
def create_column(
    board_id: int,
    payload: ColumnCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_board_or_403(board_id, user, db)
    max_pos = (
        db.query(Column)
        .filter(Column.board_id == board_id)
        .order_by(Column.position.desc())
        .first()
    )
    next_position = (max_pos.position + 1) if max_pos and max_pos.position is not None else 0
    col = Column(title=payload.title, position=next_position, board_id=board_id)
    db.add(col)
    db.commit()
    db.refresh(col)
    return col


@router.put("/{column_id}", response_model=ColumnResponse)
def update_column(
    board_id: int,
    column_id: int,
    payload: ColumnUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_board_or_403(board_id, user, db)
    col = db.query(Column).filter(Column.id == column_id, Column.board_id == board_id).first()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    if payload.title is not None:
        col.title = payload.title
    if payload.position is not None:
        col.position = payload.position
    db.commit()
    db.refresh(col)
    return col


@router.delete("/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(
    board_id: int,
    column_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_board_or_403(board_id, user, db)
    col = db.query(Column).filter(Column.id == column_id, Column.board_id == board_id).first()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    db.delete(col)
    db.commit()
    return None
