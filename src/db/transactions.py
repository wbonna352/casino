from base import session
from models import Player, Transaction, GameType
from games import play_roulette

from decimal import Decimal


def get_player(player_id: int) -> Player:
    player = Player.query.filter(Player.id == player_id).first()
    assert player is not None, "Player not exists"
    return player


def add_deposit(player_id: int, value: float) -> None:
    player = get_player(player_id)

    transaction = Transaction(
        player_id=player_id,
        type="deposit",
        value=value
    )

    session.add(transaction)
    player.account_balance += Decimal(value)
    session.commit()


def add_withdrawal(player_id: int, value: float) -> None:
    player = get_player(player_id)
    assert player.account_balance >= Decimal(value), "Too high withdrawal"
    transaction = Transaction(
        player_id=player_id,
        type="withdrawal",
        value=value
    )

    session.add(transaction)
    player.account_balance -= Decimal(value)
    session.commit()


def add_game(player_id: int, game_type: GameType, stake: float) -> None:
    player = get_player(player_id)
    assert player.account_balance >= Decimal(stake), "Too high stake"
    if game_type == GameType.roulette:
        game = play_roulette(player_id, stake)

    session.add(game)
    player.account_balance -= game.stake
    player.account_balance += game.payout
    session.commit()
