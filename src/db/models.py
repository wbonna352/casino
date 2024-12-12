from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, func
from sqlalchemy.orm import Relationship
from datetime import datetime
import enum
from random import randint
from decimal import Decimal

from db.base import Base, engine, session


class ResultType(enum.Enum):
    win = "win"
    draw = "draw"
    loss = "loss"


class GameType(enum.Enum):
    straight_roulette = "straight_roulette"
    range_roulette = "range_roulette"

    def play(self, stake) -> (ResultType, float):
        match self:
            case GameType.straight_roulette:
                number = randint(0, 36)
                result = ResultType.win if number == 0 else ResultType.loss
                payout = Decimal(36 * stake) if result == ResultType.win else 0
                return result, payout
            case GameType.range_roulette:
                number = randint(0, 36)
                result = ResultType.win if number > 18 else ResultType.loss
                payout = Decimal(2 * stake) if result == ResultType.win else 0
                return result, payout


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

    def play_game(self, game_type: GameType, stake: float) -> None:
        result, payout = game_type.play(stake)
        game = Game(
            player_id=self.id,
            type=game_type,
            stake=stake,
            result=result,
            payout=payout
        )

        session.add(game)
        self.account_balance -= game.stake
        self.account_balance += game.payout
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
