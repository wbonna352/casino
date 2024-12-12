import os
from random import choice
from time import sleep
from random import randint
from db.transactions import is_player_exists, get_player_by_email
from db.base import session
from db.models import Player, GameType

email: str = os.getenv("PLAYER_EMAIL")


def strategy(player: Player) -> None:
    match player.email:
        case "ethan.clark@example.com":
            sleep(randint(1, 60))
            stake = max(player.account_balance * randint(5, 50) / 100, 1)
            player.play_game(GameType.range_roulette, stake)
        case "olivia.bennett@example.com":
            sleep(randint(1, 15))
            stake = max(player.account_balance * randint(1, 10) / 100, 1)
            player.play_game(GameType.straight_roulette, stake)
        case "lucas.hayes@example.com":
            sleep(randint(10, 60))
            type = choice(list(GameType))
            match type:
                case GameType.straight_roulette:
                    stake = max(player.account_balance * randint(1, 5) / 100, 1)
                case GameType.range_roulette:
                    stake = max(player.account_balance * randint(5, 50) / 100, 1)
            player.play_game(type, stake)


if __name__ == '__main__':

    if not is_player_exists(email):
        session.add(Player(
            first_name=os.getenv("PLAYER_FIRST_NAME"),
            last_name=os.getenv("PLAYER_LAST_NAME"),
            email=email
        ))
        session.commit()

    player: Player = get_player_by_email(email)

    if player.account_balance <= 1:
        sleep(randint(10, 120))
        player.make_deposit(1000)

    while player.account_balance >= 1:
        strategy(player)
