from models import Game, ResultType, GameType
from decimal import Decimal
from random import randint


def play_straight_roulette(player_id: int, stake: float) -> Game:
    number = randint(0, 36)
    result = ResultType.win if number == 0 else ResultType.loss
    payout = Decimal(36 * stake) if result == ResultType.win else 0

    return Game(
        player_id=player_id,
        type=GameType.straight_roulette,
        stake=stake,
        result=result,
        payout=payout
    )


def play_range_roulette(player_id: int, stake: float) -> Game:
    number = randint(0, 36)
    result = ResultType.win if number > 18 else ResultType.loss
    payout = Decimal(2 * stake) if result == ResultType.win else 0

    return Game(
        player_id=player_id,
        type=GameType.range_roulette,
        stake=stake,
        result=result,
        payout=payout
    )
