from base import session
from models import Player, Transaction, GameType
from games import play_straight_roulette, play_range_roulette

from decimal import Decimal


def get_player_by_email(email: str) -> Player:
    return Player.query.filter(Player.email == email).first()


def is_player_exists(email: str) -> bool:
    return bool(get_player_by_email(email))


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
    if game_type == GameType.straight_roulette:
        game = play_straight_roulette(player_id, stake)
    elif game_type == GameType.range_roulette:
        game = play_range_roulette(player_id, stake)

    session.add(game)
    player.account_balance -= game.stake
    player.account_balance += game.payout
    session.commit()
