from sqlalchemy import Column as SAColumn
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = SAColumn(Integer, primary_key=True, index=True)
    username = SAColumn(String(50), unique=True, index=True, nullable=False)
    hashed_password = SAColumn(String(128), nullable=False)

    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")


class Board(Base):
    __tablename__ = "boards"

    id = SAColumn(Integer, primary_key=True, index=True)
    title = SAColumn(String(100), nullable=False)
    owner_id = SAColumn(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="boards")
    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan")


class Column(Base):
    __tablename__ = "columns"

    id = SAColumn(Integer, primary_key=True, index=True)
    title = SAColumn(String(100), nullable=False)
    position = SAColumn(Integer, nullable=False, default=0)
    board_id = SAColumn(Integer, ForeignKey("boards.id"), nullable=False)

    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"

    id = SAColumn(Integer, primary_key=True, index=True)
    title = SAColumn(String(200), nullable=False)
    description = SAColumn(String(2000), default="")
    position = SAColumn(Integer, nullable=False, default=0)
    column_id = SAColumn(Integer, ForeignKey("columns.id"), nullable=False)

    column = relationship("Column", back_populates="cards")
