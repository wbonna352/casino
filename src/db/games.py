from models import Game, ResultType, GameType
from decimal import Decimal
from random import randint


def play_roulette(player_id: int, stake: float) -> Game:
    number = randint(0, 36)
    result = ResultType.win if number == 0 else ResultType.loss
    payout = Decimal(35 * stake) if result == ResultType.win else 0

    return Game(
        player_id=player_id,
        type=GameType.roulette,
        stake=stake,
        result=result,
        payout=payout
    )
