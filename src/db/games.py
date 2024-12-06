from models import Game, ResultType, GameType, Player
from base import session
from decimal import Decimal
from random import randint


def play_straight_roulette(player_id: int, stake: float) -> None:

    player = Player.query.filter(Player.id == player_id).first()
    number = randint(0, 36)
    result = ResultType.win if number == 0 else ResultType.loss
    payout = Decimal(36 * stake) if result == ResultType.win else 0
    game = Game(
        player_id=player_id,
        type=GameType.straight_roulette,
        stake=stake,
        result=result,
        payout=payout
    )

    session.add(game)
    player.account_balance -= game.stake
    player.account_balance += game.payout
    session.commit()


def play_range_roulette(player_id: int, stake: float) -> None:
    player = Player.query.filter(Player.id == player_id).first()
    number = randint(0, 36)
    result = ResultType.win if number > 18 else ResultType.loss
    payout = Decimal(2 * stake) if result == ResultType.win else 0

    game = Game(
        player_id=player_id,
        type=GameType.range_roulette,
        stake=stake,
        result=result,
        payout=payout
    )

    session.add(game)
    player.account_balance -= game.stake
    player.account_balance += game.payout
    session.commit()
