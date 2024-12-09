from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, func
from sqlalchemy.orm import Relationship
from datetime import datetime
import enum
from decimal import Decimal

from base import Base, engine, session


class GameType(enum.Enum):
    straight_roulette = "straight_roulette"
    range_roulette = "range_roulette"


class ResultType(enum.Enum):
    win = "win"
    draw = "draw"
    loss = "loss"


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

    def make_deposit(self, value: float) -> None:
        transaction = Transaction(
            player_id=self.id,
            type=TransactionType.deposit,
            value=value
        )
        session.add(transaction)
        self.account_balance += Decimal(value)
        session.commit()

    def make_withdrawal(self, value: float) -> None:
        transaction = Transaction(
            player_id=self.id,
            type=TransactionType.withdrawal,
            value=value
        )
        assert self.account_balance >= Decimal(value), "Too high withdrawal"
        session.add(transaction)
        self.account_balance -= Decimal(value)
        session.commit()


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


def create_tables() -> None:
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
