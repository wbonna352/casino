from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, func
from sqlalchemy.orm import Relationship
from datetime import datetime
import enum

from base import Base, engine


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    account_balance = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    transaction = Relationship("Transaction", back_populates="player")
    game = Relationship("Game", back_populates="player")


class TransactionType(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    player = Relationship("Player", back_populates="transaction")


class GameType(enum.Enum):
    roulette = "roulette"


class ResultType(enum.Enum):
    win = "win"
    draw = "draw"
    loss = "loss"


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    type = Column(Enum(GameType), nullable=False)
    stake = Column(Numeric(10, 2), nullable=False)
    result = Column(Enum(ResultType), nullable=False)
    payout = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    player = Relationship("Player", back_populates="game")


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
