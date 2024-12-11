import os
from time import sleep
from random import randint
from transactions import is_player_exists, get_player_by_email
from base import session
from models import Player, create_tables
from games import play_range_roulette
import models

email: str = os.getenv("PLAYER_EMAIL")

if __name__ == '__main__':

    create_tables()

    if not is_player_exists(email):
        session.add(Player(
            first_name=os.getenv("PLAYER_FIRST_NAME"),
            last_name=os.getenv("PLAYER_LAST_NAME"),
            email=email
        ))
        session.commit()

    player: Player = get_player_by_email(email)

    if player.account_balance <= 1:
        player.make_deposit(1000)

    while player.account_balance >= 1:
        stake = max(player.account_balance * randint(5, 50) / 100, 1)
        play_range_roulette(player.id, stake)
        sleep(randint(1, 120))
