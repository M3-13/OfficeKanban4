from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Board, Column, User
from ..schemas import BoardCreate, BoardResponse, BoardUpdate

router = APIRouter(prefix="/boards", tags=["boards"])

DEFAULT_COLUMNS = [
    {"title": "To Do", "position": 0},
    {"title": "In Progress", "position": 1},
    {"title": "Done", "position": 2},
]


@router.get("", response_model=list[BoardResponse])
def list_boards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Board).filter(Board.owner_id == current_user.id).order_by(Board.title).all()


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    payload: BoardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    board = Board(title=payload.title, owner_id=current_user.id)
    db.add(board)
    db.flush()
    for col in DEFAULT_COLUMNS:
        db.add(Column(title=col["title"], position=col["position"], board_id=board.id))
    db.commit()
    db.refresh(board)
    return board


@router.get("/{board_id}", response_model=BoardResponse)
def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return board


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    payload: BoardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    board.title = payload.title
    db.commit()
    db.refresh(board)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    board = db.query(Board).filter(Board.id == board_id).first()
    if board is None or board.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    db.delete(board)
    db.commit()
